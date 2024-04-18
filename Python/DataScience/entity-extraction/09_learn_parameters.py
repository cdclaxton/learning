# Learn the parameters of the likelihood function
import random
import numpy as np
from typing import Callable, List, Tuple
from domain import Tokens, assert_tokens_valid
from lookup.lmdb_lookup import LmdbLookup
from lookup.lookup import Lookup
from scipy.optimize import minimize, Bounds


def mutate(tokens: Tokens) -> Tokens:
    """Mutate tokens by adding and removing tokens."""

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
    n_tokens_to_add = random.randint(0, 2)

    # Add tokens at random
    for i in range(n_tokens_to_add):
        idx = random.randint(1, len(mutated_tokens) - 1)
        mutated_tokens.insert(idx, f"--({i})--")

    assert_tokens_valid(mutated_tokens)
    return mutated_tokens


def num_adds_removes(tokens: Tokens, entity: Tokens) -> Tuple[int, int]:
    """Number of tokens added and removed."""

    assert_tokens_valid(tokens)
    assert_tokens_valid(entity)

    set_tokens = set(tokens)
    set_entity = set(entity)

    n_adds = len(set_tokens.difference(set_entity))
    n_removes = len(set_entity.difference(set_tokens))

    return n_adds, n_removes


def entity_matches(tokens: Tokens, lookup: Lookup) -> List[Tuple[int, int, int]]:
    """Returns the number of adds and removes for a given list of tokens."""

    assert_tokens_valid(tokens)
    assert isinstance(lookup, Lookup)

    # Set of all entity IDs given the tokens
    entity_ids = set()
    for token in tokens:
        entities = lookup.entity_ids_for_token(token)
        if entities is not None:
            entity_ids.update(entities)

    assert len(entity_ids) > 0

    # Walk through each matching entity and count the number of adds and removes
    result = []
    for entity_id in entity_ids:
        entity_tokens = lookup.tokens_for_entity(entity_id)
        assert entity_tokens is not None

        n_adds, n_removes = num_adds_removes(tokens, entity_tokens)
        result.append((entity_id, n_adds, n_removes))

    return result


def build_dataset(
    lookup: Lookup, n_samples: int
) -> Tuple[List[Tuple[int, int]], List[List[Tuple[int, int, int]]]]:
    """Build a dataset for training."""

    assert isinstance(lookup, Lookup)
    assert type(n_samples) == int and n_samples > 0

    # Maximum internal entity ID
    max_entity_id = lookup.max_entity_id()
    assert max_entity_id > 0

    # Entity IDs of entities to use (note that an entity can be selected more
    # than once)
    entity_ids = [random.randint(0, max_entity_id) for _ in range(n_samples)]

    # Mutate tokens for each entity
    entity_ids_token_count: List[Tuple[int, int]] = []
    result: List[List[Tuple[int, int, int]]] = []
    for entity_id in entity_ids:

        # Get the tokens for the entity from the lookup
        tokens = lookup.tokens_for_entity(entity_id)
        assert tokens is not None, f"no tokens for entity with ID={entity_id}"
        assert_tokens_valid(tokens)

        # Store the entity ID and the number of tokens for the entity
        entity_ids_token_count.append((entity_id, len(tokens)))

        # Mutate tokens
        mutated_tokens = mutate(tokens)

        # Find the number of adds and removes for the matching entities
        result.append(entity_matches(mutated_tokens, lookup))

    return entity_ids_token_count, result


def calc_error(
    expected_entity: int,
    n_tokens_expected_entity: int,
    entity_matches: List[Tuple[int, int, int]],
    likelihood: Callable[[float, float], float],
) -> float:
    """Calculate the error."""

    # Calculate the likelihood of each entity
    likelihoods = {}
    for entity_id, n_adds, n_removes in entity_matches:
        likelihoods[entity_id] = likelihood(
            n_adds / n_tokens_expected_entity, n_removes / n_tokens_expected_entity
        )

    assert expected_entity in likelihoods
    expected_entity_prob = likelihoods[expected_entity]

    # Number of entities with a higher likelihood than the expected entity
    n_higher = 0
    n_equal = 0
    n_lower = 0

    for actual_entity, prob in likelihoods.items():
        if actual_entity == expected_entity:
            continue

        if prob > expected_entity_prob:
            n_higher += 1
        elif prob < expected_entity_prob:
            n_lower += 1
        else:
            n_equal += 1

    return n_higher + n_equal


def linear(x0, y0, x1, y1, x):
    return ((y1 - y0) / (x1 - x0)) * (x - x0) + y0


def build_likelihood_function(
    x: List[float], y: List[float]
) -> Callable[[float, float], float]:
    """Build a symmetric likelihood function."""

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
        prop = min(prop, 1.0)

        if prop < x[0]:
            return linear(0, 1, x[0], y[0], prop)
        elif prop >= x[-1]:
            return linear(x[-1], y[-1], 1, 0, prop)

        for i in range(len(x) - 1):
            if x[i] <= prop < x[i + 1]:
                return linear(x[i], y[i], x[i + 1], y[i + 1], prop)

        return -1.0

    def likelihood(prop_adds: float, prop_removes: float) -> float:
        p_adds = f(prop_adds)
        assert p_adds >= 0.0, f"p_adds={p_adds}"

        p_removes = f(prop_removes)
        assert p_removes >= 0.0, f"p_removes={p_removes}"

        return p_adds * p_removes

    return likelihood


def total_error(
    entity_ids_token_count: List[Tuple[int, int]],
    entity_add_removes: List[List[Tuple[int, int, int]]],
    x: List[float],
    y: List[float],
) -> float:

    assert len(entity_ids_token_count) == len(entity_add_removes)
    assert len(x) == len(y)

    # Make the likelihood function
    likelihood_fn = build_likelihood_function(x, y)

    # Calculate the error for each entity
    total = 0.0
    for i in range(len(entity_ids_token_count)):
        expected_entity, n_tokens_expected_entity = entity_ids_token_count[i]

        total += calc_error(
            expected_entity=expected_entity,
            n_tokens_expected_entity=n_tokens_expected_entity,
            entity_matches=entity_add_removes[i],
            likelihood=likelihood_fn,
        )

    return total


def learn(
    entity_ids_token_count: List[Tuple[int, int]],
    entity_add_removes: List[List[Tuple[int, int, int]]],
    points: List[float],
) -> List[float]:

    # Starting position
    x0 = 0.5 * np.ones(len(points))

    # Bounds
    lower = np.zeros(len(points))
    upper = np.ones(len(points))
    bounds = Bounds(lower, upper)

    def f(x):
        """Function to minimise."""
        return total_error(entity_ids_token_count, entity_add_removes, points, list(x))

    res = minimize(f, x0, method="trust-constr", bounds=bounds, options={"disp": True})

    return res.x


if __name__ == "__main__":

    # Initialise a lookup for reading
    lmdb_folder = "./data/lmdb"
    lookup = LmdbLookup(lmdb_folder, False)

    # Build the dataset from which to learn the parameters
    entity_ids_token_count, entity_add_removes = build_dataset(lookup, 2)

    # Learn the parameters using optimisation
    points = [0.3, 0.7]
    y = learn(entity_ids_token_count, entity_add_removes, points)
    print(f"y values: {y}")

    # 18/04/24: 0h20
