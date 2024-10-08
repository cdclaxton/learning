# Learn the parameters of the likelihood function
import random
import math
import numpy as np
import pickle
import statistics
import sys
import time

from typing import Callable, Dict, List, Tuple
from domain import Tokens, assert_tokens_valid
from lookup.lmdb_lookup import LmdbLookup
from lookup.lookup import Lookup
from scipy import optimize
from loguru import logger
from scipy import stats


def mutate(tokens: Tokens, min_tokens: int) -> Tokens:
    """Mutate tokens by adding and removing tokens."""

    assert_tokens_valid(tokens)
    assert type(min_tokens) == int and min_tokens > 0

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

    set_tokens = set(tokens)  # Set of tokens in the text
    set_entity = set(entity)  # Set of tokens in the entity

    n_adds = len(set_tokens.difference(set_entity))
    n_removes = len(set_entity.difference(set_tokens))

    return n_adds, n_removes


def entity_matches(
    tokens: Tokens, lookup: Lookup, min_count: int
) -> List[Tuple[int, int, int]]:
    """Returns the number of adds and removes for a given list of tokens."""

    assert_tokens_valid(tokens)
    assert isinstance(lookup, Lookup)
    assert type(min_count) == int and min_count > 0

    # Dict of all entity IDs given the tokens to their count
    entity_id_to_count: Dict[int, int] = dict()
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

    # Walk through each matching entity and count the number of adds and removes
    result = []
    for entity_id, count in entity_id_to_count.items():
        if count < min_count:
            continue

        entity_tokens = lookup.tokens_for_entity(entity_id)
        assert entity_tokens is not None

        n_adds, n_removes = num_adds_removes(tokens, entity_tokens)
        result.append((entity_id, n_adds, n_removes))

    return result


def build_dataset(
    lookup: Lookup,
    n_samples: int,
    min_tokens: int,
    min_count: int,
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
    for idx, entity_id in enumerate(entity_ids):

        # Get the tokens for the entity from the lookup
        tokens = lookup.tokens_for_entity(entity_id)
        logger.debug(f"[{idx+1}/{n_samples}] Tokens for entity {entity_id}: {tokens}")
        assert tokens is not None, f"no tokens for entity with ID={entity_id}"
        assert_tokens_valid(tokens)

        # Store the entity ID and the number of tokens for the entity
        entity_ids_token_count.append((entity_id, len(tokens)))

        # Mutate tokens
        mutated_tokens = mutate(tokens, min_tokens)
        logger.debug(
            f"[{idx+1}/{n_samples}] Mutated tokens for entity {entity_id}: {mutated_tokens}"
        )

        # Find the number of adds and removes for the matching entities
        matches = entity_matches(mutated_tokens, lookup, min_count)

        # Ensure the entity made it through to the matches
        found = False
        for matched_entity_id, _, _ in matches:
            if entity_id == matched_entity_id:
                found = True

        assert found, f"Entity {entity_id} is not included in the matches"

        # Store the matches
        result.append(matches)
        logger.debug(
            f"[{idx+1}/{n_samples}] Number of matches for entity {entity_id}: {len(matches)}"
        )

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

    assert (
        expected_entity in likelihoods
    ), f"Failed to find expected entity {expected_entity} in likelihoods"
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

    return 2 * n_higher + n_equal


def linear(x0, y0, x1, y1, x):
    # To avoid floating point rounding issues
    if x == x0:
        return y0
    elif x == x1:
        return y1

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
    assert len(x) == len(y), f"differing number of points: {len(x)} vs {len(y)}"

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
    bounds = optimize.Bounds(lower, upper)

    def f(x):
        """Function to minimise."""
        e = total_error(entity_ids_token_count, entity_add_removes, points, list(x))
        logger.debug(f"x = {x}, total error = {e}")
        return e

    # res = minimize(f, x0, method="trust-constr", bounds=bounds, options={"disp": True})
    # return res.x

    # res = optimize.shgo(f, bounds)

    # Global optimisation
    # res = optimize.dual_annealing(f, bounds)
    # print(res)
    # return res.x

    # Brute-force optimisation
    rranges = [slice(0, 1, 0.1) for _ in range(len(points))]
    res_brute = optimize.brute(f, rranges, full_output=True, finish=None)

    return res_brute[0]


def learn2(
    entity_ids_token_count: List[Tuple[int, int]],
    entity_add_removes: List[List[Tuple[int, int, int]]],
    n_points: int,
) -> Tuple[List[float], List[float]]:

    assert type(n_points) == int and n_points > 0

    def decreasing(x):
        return all([x[i] > x[i + 1] for i in range(len(x) - 1)])

    def increasing(x):
        return all([x[i] < x[i + 1] for i in range(len(x) - 1)])

    def f(x):
        x_pos = x[:n_points]
        y_pos = x[n_points:]

        if not increasing(x_pos) or not decreasing(y_pos):
            return np.inf

        e = total_error(
            entity_ids_token_count, entity_add_removes, list(x_pos), list(y_pos)
        )
        logger.debug(f"x = {x_pos}, y = {y_pos}, total error = {e}")
        return e

    # Brute-force optimisation
    x_delta = 0.1
    x_pos_ranges = [slice(x_delta, 1 + x_delta, x_delta) for _ in range(len(points))]

    y_delta = 0.1
    y_pos_ranges = [slice(0, 1, y_delta) for _ in range(len(points))]

    rranges = x_pos_ranges[:]
    rranges.extend(y_pos_ranges)

    res_brute = optimize.brute(f, rranges, full_output=True, finish=None)

    return res_brute[0][:n_points], res_brute[0][n_points:]


def build_dataset_from_lookup(
    lmdb_folder: str, n_samples: int, min_tokens: int, min_count: int, filepath: str
) -> None:
    """Build a dataset of n_samples samples using an LMDB lookup."""

    assert type(lmdb_folder) == str
    assert type(n_samples) == int and n_samples > 0
    assert type(min_tokens) == int and min_tokens > 0
    assert type(min_count) == int and min_count > 0
    assert type(filepath) == str

    # Initialise a lookup for reading
    lookup = LmdbLookup(lmdb_folder, False)

    # Build the dataset from which to learn the parameters
    logger.info(f"Building dataset with {n_samples} samples")
    entity_ids_token_count, entity_add_removes = build_dataset(
        lookup, n_samples, min_tokens, min_count
    )

    dataset = {
        "entity_ids_token_count": entity_ids_token_count,
        "entity_add_removes": entity_add_removes,
    }

    # Pickle the dataset
    logger.info(f"Writing dataset to file: {filepath}")
    with open(filepath, "wb") as fp:
        pickle.dump(dataset, fp)


def read_dataset(filepath: str):
    """Read the dataset from a Pickle file."""

    # Load the data from file
    logger.info(f"Loading dataset from file: {filepath}")
    with open(filepath, "rb") as fp:
        dataset = pickle.load(fp)

    entity_ids_token_count: List[Tuple[int, int]] = dataset["entity_ids_token_count"]
    entity_add_removes: List[List[Tuple[int, int, int]]] = dataset["entity_add_removes"]

    return entity_ids_token_count, entity_add_removes


def sample_error(
    entity_ids_token_count: List[Tuple[int, int]],
    entity_add_removes: List[List[Tuple[int, int, int]]],
    likelihood_fn: Callable[[float, float], float],
) -> List[float]:
    """Calculates the error for each sample given the likelihood function."""

    n = len(entity_ids_token_count)

    errors = [0.0 for _ in range(n)]
    for i in range(n):
        expected_entity, n_tokens_expected_entity = entity_ids_token_count[i]

        errors[i] = calc_error(
            expected_entity=expected_entity,
            n_tokens_expected_entity=n_tokens_expected_entity,
            entity_matches=entity_add_removes[i],
            likelihood=likelihood_fn,
        )

    return errors


def linear_likelihood(prop_adds: float, prop_removes: float) -> float:
    """Straight line likelihood function."""

    p_adds = linear(x0=0.0, y0=1.0, x1=1.0, y1=0.0, x=prop_adds)
    p_removes = linear(x0=0.0, y0=1.0, x1=1.0, y1=0.0, x=prop_removes)
    return p_adds * p_removes


def calc_p_value(before, after) -> Tuple[float, str]:
    assert len(before) == len(after)
    assert len(before) > 0

    n = len(before)

    diffs = np.array(after) - np.array(before)

    # Sample means
    x_bar = statistics.mean(diffs)

    # Sample standard deviation
    s_d = math.sqrt(statistics.variance(diffs))

    # Number of degrees of freedom
    df = n - 1

    # t test statistic
    t = x_bar / (s_d / math.sqrt(n))
    p_value = stats.t.cdf(t, df)
    alpha = 0.05
    if p_value < alpha:
        msg = "Reject the null hypothesis that there is no difference"
    else:
        msg = "Accept the null hypothesis that there is no difference"

    return (p_value, msg)


if __name__ == "__main__":

    valid_modes = {"build-train", "build-eval", "learn", "eval"}

    if len(sys.argv) != 2 or sys.argv[1] not in valid_modes:
        print(f"Usage: python3 {sys.argv[0]} <mode>")
        print("Modes:")
        print("  build-train - build the training set")
        print("  build-eval  - build the evaluation set")
        print("  learn       - learn the parameters of the likelihood function")
        print("  eval        - evaluate the performance using the evaluate set")
        exit(-1)

    # File paths for the training and evaluation data
    training_filepath = "./data/training-data.pickle"
    evaluation_filepath = "./data/evaluation-data.pickle"

    # Location of the LMDB data
    lmdb_folder = "./data/lmdb"

    # Minimum number of tokens for an entity to be considered as existing
    min_tokens = 3

    # Minimum number of tokens that an entity must match
    min_count = 3

    # Locations of the changes in the piecewise likelihood function
    points = [0.3, 0.7]

    start_time = time.time()

    mode = sys.argv[1]
    if mode == "build-train":

        # Number of samples to generate to use in the optimisation step
        n_samples = 2

        # Build the dataset from which to learn the parameters
        build_dataset_from_lookup(
            lmdb_folder, n_samples, min_tokens, min_count, training_filepath
        )

    elif mode == "build-eval":

        # Number of samples to generate to use in the evaluation step
        n_samples = 2

        # Build the dataset from which to evaluate the parameters
        build_dataset_from_lookup(
            lmdb_folder, n_samples, min_tokens, min_count, evaluation_filepath
        )

    elif mode == "learn":

        # Load the data from file
        entity_ids_token_count, entity_add_removes = read_dataset(training_filepath)

        # Learn the parameters using optimisation
        logger.info("Learning parameters")

        # y = learn(entity_ids_token_count, entity_add_removes, points)
        # logger.info(f"y values: {y}")

        x, y = learn2(entity_ids_token_count, entity_add_removes, 2)
        logger.info(f"x values: {x}, y values: {y}")

    elif mode == "eval":

        # Load the data from file
        entity_ids_token_count, entity_add_removes = read_dataset(evaluation_filepath)

        # Calculate the total error given the linear likelihood model
        es = sample_error(entity_ids_token_count, entity_add_removes, linear_likelihood)
        logger.info(f"Error for linear likelihood = {sum(es)}")

        evaluation_sets = [
            {
                "description": "original",
                "x": [0.3, 0.7],
                "y": [0.7, 0.5],
            },
            {
                "description": "optimised with two points (1)",
                "x": [0.3, 0.7],
                "y": [0.6, 0.5],
            },
            {
                "description": "optimised with two points (2)",
                "x": [0.25, 0.50],
                "y": [0.4, 0.3],
            },
            {
                "description": "optimised with three points",
                "x": [0.25, 0.50, 0.75],
                "y": [0.6, 0.5, 0.5],
            },
            {
                "description": "optimising for x and y",
                "x": [0.3, 0.9],
                "y": [0.7, 0.6],
            },
        ]

        for eval_set in evaluation_sets:
            err = total_error(
                entity_ids_token_count, entity_add_removes, eval_set["x"], eval_set["y"]
            )
            logger.info(
                f"Error for '{eval_set['description']}': x = {eval_set['x']}, y = {eval_set['y']}, total error = {err}"
            )

            # Make a likelihood function given the points in the evaluation set
            f = build_likelihood_function(eval_set["x"], eval_set["y"])

            error_linear = sample_error(
                entity_ids_token_count, entity_add_removes, linear_likelihood
            )
            error_set = sample_error(entity_ids_token_count, entity_add_removes, f)

            # Determine if the difference in the error is statistically
            # significant compared to the linear model
            p_value, msg = calc_p_value(error_linear, error_set)
            logger.info(f"p-value: {p_value}, {msg}")

    end_time = time.time()
    logger.info(f"Execution time = {end_time - start_time} seconds")
