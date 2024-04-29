# This script explores the probability p(E_i | T), which is the probability that
# the text T contains entity E_i.

import random


from dataclasses import dataclass
import sys
from typing import Callable
from domain import Tokens, assert_tokens_valid
from loguru import logger
from lookup.lmdb_lookup import LmdbLookup
from lookup.lookup import Lookup


def mutate(tokens: Tokens, min_tokens: int, max_additions: int) -> Tokens:
    """Mutate an entity's tokens by adding and removing tokens."""

    assert_tokens_valid(tokens)
    assert type(min_tokens) == int and min_tokens > 0
    assert type(max_additions) == int and max_additions >= 0

    # Make a copy of the tokens
    mutated_tokens = tokens[:]

    # Number of tokens to remove
    max_tokens_to_remove = max(0, len(mutated_tokens) - 3)
    n_tokens_to_remove = random.randint(0, max_tokens_to_remove)

    # Remove tokens at random
    for _ in range(n_tokens_to_remove):
        idx = random.randint(0, len(mutated_tokens) - 1)
        del mutated_tokens[idx]

    # Number of tokens to add
    n_tokens_to_add = random.randint(0, max_additions)

    # Add tokens at random
    for i in range(n_tokens_to_add):
        idx = random.randint(1, len(mutated_tokens) - 1)
        mutated_tokens.insert(idx, f"--({i})--")

    assert_tokens_valid(mutated_tokens)
    return mutated_tokens


@dataclass
class Match:
    entity_id: int  # Entity ID
    n_matches: int  # Number of tokens that match the entity
    n_additions: int  # Number of additional tokens compared to the entity
    n_removals: int  # Number of tokens removed from the entity
    n_entity_tokens: int  # Number of tokens in the entity


@dataclass
class Sample:
    entity_id: int  # Ground truth entity ID
    n_tokens: int  # Number of tokens in the ground truth entity
    matches: list[Match]  # Entity matches


def num_matches_additions(
    ground_truth_tokens: Tokens, entity_tokens: Tokens
) -> tuple[int, int, int]:
    """Number of token matches, number of additions and number of removals."""

    assert_tokens_valid(ground_truth_tokens)
    assert_tokens_valid(entity_tokens)

    set_ground_truth = set(ground_truth_tokens)
    set_entity = set(entity_tokens)

    n_matches = len(set_ground_truth.intersection(set_entity))
    n_additions = len(set_entity.difference(set_entity))
    n_removals = len(set_entity.difference(set_entity))

    assert n_matches > 0
    assert n_additions >= 0
    assert n_removals >= 0

    return n_matches, n_additions, n_removals


def entity_matches(tokens: Tokens, lookup: Lookup, min_tokens: int) -> list[Match]:

    assert_tokens_valid(tokens)
    assert isinstance(lookup, Lookup)
    assert type(min_tokens) == int and min_tokens > 0

    # Dict of all entity IDs given the tokens to their count
    entity_id_to_count: dict[int, int] = dict()
    for token in tokens:
        entities = lookup.entity_ids_for_token(token)
        if entities is None:
            continue

        for entity_id in entities:
            if entity_id in entity_id_to_count:
                entity_id_to_count[entity_id] += 1
            else:
                entity_id_to_count[entity_id] = 1

    assert len(entity_id_to_count) > 0

    # Walk through each matching entity
    matches: list[Match] = []
    for entity_id, count in entity_id_to_count.items():
        if count < min_tokens:
            continue

        entity_tokens = lookup.tokens_for_entity(entity_id)
        assert entity_tokens is not None

        n_matches, n_additions, n_removals = num_matches_additions(
            tokens, entity_tokens
        )
        matches.append(
            Match(entity_id, n_matches, n_additions, n_removals, len(entity_tokens))
        )

    assert len(matches) > 0
    return matches


def build_dataset(
    lookup: Lookup, n: int, min_tokens: int, max_additions: int
) -> list[Sample]:
    """Build a dataset of n samples given a lookup."""

    samples: list[Sample] = []

    # Maximum internal entity ID
    max_entity_id = lookup.max_entity_id()
    assert max_entity_id > 0

    # Generate n samples
    for idx in range(n):

        # Randomly select an entity from the lookup
        entity_id = random.randint(0, max_entity_id)

        # Get the tokens for the entity from the lookup
        tokens = lookup.tokens_for_entity(entity_id)
        logger.debug(f"[{idx+1}/{n}] Tokens for entity {entity_id}: {tokens}")
        assert tokens is not None, f"no tokens for entity with ID={entity_id}"
        assert_tokens_valid(tokens)

        # Mutate tokens to generate a synthetic piece of tokenised text
        mutated_tokens = mutate(tokens, min_tokens, max_additions)
        logger.debug(
            f"[{idx+1}/{n}] Mutated tokens for entity {entity_id}: {mutated_tokens}"
        )

        # Find the matching entities
        matches: list[Match] = entity_matches(mutated_tokens, lookup, min_tokens)

        # Ensure the ground truth entity is present in the matches
        found = False
        for m in matches:
            if m.entity_id == entity_id:
                found = True

        assert found, f"Entity {entity_id} is not included in the matches"

        # Store the sample
        samples.append(Sample(entity_id, len(tokens), matches))

    return samples


def calc_error(
    sample: Sample,
    likelihood: Callable[[Match], float],
) -> float:

    # Calculate the likelihood of each entity
    likelihoods = {}
    for match in sample.matches:
        likelihoods[match.entity_id] = likelihood(match)

    assert (
        sample.entity_id in likelihoods
    ), f"Failed to find expected entity {sample.entity_id} in likelihoods"
    expected_entity_prob = likelihoods[sample.entity_id]

    # Number of entities with a higher likelihood than the expected entity
    n_higher = 0
    n_equal = 0
    n_lower = 0

    for actual_entity, prob in likelihoods.items():
        if actual_entity == sample.entity_id:
            continue

        if prob > expected_entity_prob:
            n_higher += 1
        elif prob < expected_entity_prob:
            n_lower += 1
        else:
            n_equal += 1

    return 2 * n_higher + n_equal


def total_error(dataset: list[Sample], likelihood: Callable[[Match], float]) -> float:
    """Calculate the total error for the dataset and the likelihood function."""

    return sum([calc_error(sample, likelihood) for sample in dataset])


def build_likelihood1(min_tokens: int, max_additions: int) -> Callable[[Match], float]:
    """Build a likelihood function of the form p(T_m|N_i) * p(T_a)."""

    assert type(min_tokens) == int and min_tokens > 0
    assert type(max_additions) == int and max_additions >= 0

    def f(match: Match) -> float:
        if match.n_additions > max_additions or match.n_matches < min_tokens:
            return 0.0

        p_ta = 1.0 / (max_additions + 1)
        p_m = 1.0 / (match.n_entity_tokens - min_tokens + 1)

        return p_ta * p_m

    return f


def linear(x0, y0, x1, y1, x):
    # To avoid floating point rounding issues
    if x == x0:
        return y0
    elif x == x1:
        return y1

    return ((y1 - y0) / (x1 - x0)) * (x - x0) + y0


def build_likelihood2(
    min_tokens: int, x: list[float], y: list[float]
) -> Callable[[Match], float]:
    """Build a likelihood function."""

    assert len(x) > 0
    assert len(x) == len(y), f"differing lengths: {len(x)} vs {len(y)}"
    assert all([0.0 <= xi <= 1.0 for xi in x]), f"invalid x positions: {x}"
    assert all([0.0 <= yi <= 1.0 for yi in y]), f"invalid y positions: {y}"

    # Allow the x positions to be unsorted
    pairs = [(x[i], y[i]) for i in range(len(x))]
    pairs = sorted(pairs, key=lambda y: y[0])

    x = [xi for xi, _ in pairs]
    y = [yi for _, yi in pairs]

    def f(prop: float) -> float:
        """Piecewise linear function."""

        # Ensure the proportion doesn't exceed 1
        prop = min(prop, 1.0)

        if prop < x[0]:
            return linear(0, 1, x[0], y[0], prop)
        elif prop >= x[-1]:
            return linear(x[-1], y[-1], 1, 0, prop)

        for i in range(len(x) - 1):
            if x[i] <= prop < x[i + 1]:
                return linear(x[i], y[i], x[i + 1], y[i + 1], prop)

        return -1.0

    def likelihood(match: Match) -> float:

        if match.n_entity_tokens < match.n_matches:
            return 0.0

        # Calculate the proportion of tokens added and removed
        p_adds = match.n_additions / match.n_entity_tokens
        p_removes = match.n_removals / match.n_entity_tokens

        assert p_adds >= 0.0, f"p_adds={p_adds}"
        assert p_removes >= 0.0, f"p_removes={p_removes}"

        return p_adds * p_removes

    return likelihood


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <number of samples>")
        exit(-1)

    n_samples = int(sys.argv[1])

    min_tokens = 3
    max_additions = 3
    x = [0.3, 0.7]
    y = [0.7, 0.5]

    # Initialise a lookup for reading
    logger.info("Initialising LMDB-based lookup")
    lookup = LmdbLookup("./data/lmdb", False)

    # Randomly select entities from the database via the lookup and mutate the
    # tokens for the entities
    dataset = build_dataset(lookup, n=n_samples, min_tokens=3, max_additions=3)
    logger.info(f"Generated a dataset with {len(dataset)} samples")

    # Calculate the total error for the dataset using likelihood function 1
    error_likelihood_fn1 = total_error(
        dataset, build_likelihood1(min_tokens, max_additions)
    )
    logger.info(f"Error with likelihood fn 1 = {error_likelihood_fn1}")

    # Total error for the dataset using likelihood function 2
    error_likelihood_fn2 = total_error(dataset, build_likelihood2(min_tokens, x, y))
    logger.info(f"Error with likelihood fn 2 = {error_likelihood_fn2}")
