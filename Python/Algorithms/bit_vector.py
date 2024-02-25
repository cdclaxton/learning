# There is a given number of possible values that may occur in the range
# [0, m-1].
#
# Data is generated that yields a value in the range [0, m-1]. It is known that
# only a small percentage of values occur more than a given number of times.
#
# The problem is to return the values that occurred more than the required
# number of times.

from typing import Dict, List
from BitVector import BitVector
import numpy as np
import random
import time


def generator(max_value: int) -> List[int]:
    data = []
    for i in range(max_value):
        present = np.random.binomial(1, 0.3)
        if present > 0:
            num = int(np.ceil(np.random.exponential(0.4)))
            data.extend([i for _ in range(num)])

    random.shuffle(data)
    return data


def values_over_min_dict(data: List[int], max_value: int, min_count: int) -> List[int]:
    """Returns the entries in data that occur at least min_value times."""

    d: Dict[int, int] = dict()
    for value in data:
        d[value] = d.get(value, 0) + 1

    return [key for key, value in d.items() if value >= min_count]


def values_over_min_bitvector(
    data: List[int], max_value: int, min_count: int
) -> List[int]:

    # List of bit vectors
    bvs = [BitVector(size=max_value) for _ in range(min_count)]

    for value in data:
        for i in range(min_count):
            if bvs[i][value] == 0:
                bvs[i][value] = 1
                break

    # Using bit shifting is fantastically slow!
    # result = []
    # for i in range(max_value):
    #     if bvs[-1][0] == 1:
    #         result.append(i)
    #     bvs[-1].shift_left(1)
    # return result

    return [i for i in range(max_value) if bvs[-1][i] == 1]


def run_experiment(
    fn, data: List[int], max_value: int, min_count: int, num_runs: int
) -> float:
    times = np.zeros(num_runs)
    for i in range(num_runs):
        start = time.time()
        fn(data, max_value, min_count)
        times[i] = time.time() - start

    return float(np.mean(times))


if __name__ == "__main__":

    # Generate a random dataset
    max_value = 10000000
    data = generator(max_value)

    # Check the algorithms produce consistent results
    min_count = 2
    counts_dict = values_over_min_dict(data, max_value, min_count)
    counts_bitvector = values_over_min_bitvector(data, max_value, min_count)

    counts_dict = sorted(counts_dict)
    counts_bitvector = sorted(counts_bitvector)

    assert counts_dict == counts_bitvector

    num_runs = 2
    print(
        f"Mean time using a dict:       {run_experiment(values_over_min_dict, data, max_value, min_count, num_runs)} seconds"
    )
    print(
        f"Mean time using a bit vector: {run_experiment(values_over_min_bitvector, data, max_value, min_count, num_runs)} seconds"
    )
