# Experiment to compare the performance of:
#
# 1. Plain function
# 2. Function wrapped in an LRU cache
# 3. Function implemented as a lookup

from functools import lru_cache
import math
import numpy as np
import random
import time
from typing import Callable, List, Tuple


def generate(n_range: Tuple[int, int], num: int) -> List[Tuple[int, int]]:
    """Generate a dataset of num elements."""

    dataset = []
    for _ in range(num):
        n = random.randint(n_range[0], n_range[1])
        n_present = random.randint(0, n)
        dataset.append((n_present, n))

    return dataset


def likelihood(n_present: int, n: int, k: float, x0: float) -> float:
    """Simple likelihood function."""

    assert n > 0
    assert 0 <= n_present <= n, f"n_present invalid: {n_present}, n: {n}"

    # Proportion present
    prop = n_present / n

    if prop == 1.0:
        return 1.0
    elif prop == 0.0:
        return 0.0

    return 1 / (1 + math.exp(-k * (prop - x0)))


@lru_cache(maxsize=100000)
def likelihood_lru_cache(n_present: int, n: int, k: float, x0: float) -> float:
    """Simple likelihood function."""

    assert n > 0
    assert 0 <= n_present <= n

    # Proportion present
    prop = n_present / n

    if prop == 1.0:
        return 1.0
    elif prop == 0.0:
        return 0.0

    return 1 / (1 + math.exp(-k * (prop - x0)))


def experiment_simple(
    dataset: List[Tuple[int, int]], n_range: Tuple[int, int], k: float, x0: float
) -> None:
    for n_present, n in dataset:
        likelihood(n_present, n, k, x0)


def experiment_lru_cache(
    dataset: List[Tuple[int, int]], n_range: Tuple[int, int], k: float, x0: float
) -> None:
    for n_present, n in dataset:
        likelihood_lru_cache(n_present, n, k, x0)


def build_likelihood_fn_dict(
    n_range: Tuple[int, int], k: float, x0: float
) -> Callable[[int, int], float]:
    lookup = dict()
    for n in range(n_range[0], n_range[1] + 1):
        for n_present in range(0, n + 1):
            lookup[(n_present, n)] = likelihood(n_present, n, k, x0)

    def f(n_present, n):
        return lookup[(n_present, n)]

    return f


def build_likelihood_fn_list(
    n_range: Tuple[int, int], k: float, x0: float
) -> Callable[[int, int], float]:

    # Table of n x n_present
    table = [
        [likelihood(n_present, n, k, x0) for n_present in range(0, n + 1)]
        for n in range(n_range[0], n_range[1] + 1)
    ]

    def f(n_present, n):
        n_offset = n - n_range[0]
        return table[n_offset][n_present]

    return f


def experiment_lookup_fn_dict(
    dataset: List[Tuple[int, int]], n_range: Tuple[int, int], k: float, x0: float
) -> None:
    lookup_fn = build_likelihood_fn_dict(n_range, k, x0)
    for n_present, n in dataset:
        lookup_fn(n_present, n)


def experiment_lookup_fn_list(
    dataset: List[Tuple[int, int]], n_range: Tuple[int, int], k: float, x0: float
) -> None:
    lookup_fn = build_likelihood_fn_list(n_range, k, x0)
    for n_present, n in dataset:
        lookup_fn(n_present, n)


def run_experiment(
    fn,
    dataset: List[Tuple[int, int]],
    n_range: Tuple[int, int],
    k: float,
    x0: float,
    n_runs: int,
) -> float:

    times = np.zeros(n_runs)
    for i in range(n_runs):
        start = time.time()
        fn(dataset, n_range, k, x0)
        times[i] = time.time() - start

    return float(np.mean(times))


if __name__ == "__main__":

    # Parameters of the logistic likelihood function
    k = 10.0
    x0 = 0.5

    n_range = (3, 19)

    # Generate a dataset of tuples of (n_present, n)
    dataset = generate(n_range, 1000000)

    num_runs = 5
    print(
        f"Simple function:        {run_experiment(experiment_simple, dataset, n_range, k, x0, num_runs)} seconds"
    )
    print(
        f"LRU cache function:     {run_experiment(experiment_lru_cache, dataset, n_range, k, x0, num_runs)} seconds"
    )
    print(
        f"Lookup function (dict): {run_experiment(experiment_lookup_fn_dict, dataset, n_range, k, x0, num_runs)} seconds"
    )
    print(
        f"Lookup function (list): {run_experiment(experiment_lookup_fn_list, dataset, n_range, k, x0, num_runs)} seconds"
    )
