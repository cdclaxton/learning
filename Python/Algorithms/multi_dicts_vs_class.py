import array
import ctypes
import numpy as np
import random
import time
from typing import Dict, List, Set
from collections import Counter


def generate(
    n_indices: int, max_value: int, num_values_per_index: int
) -> List[Set[int]]:
    """Generate a random dataset."""

    assert type(n_indices) == int and n_indices > 0
    assert type(max_value) == int and max_value > 0
    assert type(num_values_per_index) == int and num_values_per_index > 0
    assert num_values_per_index <= max_value

    result = []
    for _ in range(n_indices):
        s: Set[int] = set()
        while len(s) < num_values_per_index:
            s.add(random.randint(0, max_value - 1))

        result.append(s)

    return result


def multi_dicts(dataset: List[Set[int]], max_value: int) -> None:
    counts: Dict[int, int] = dict()
    start: Dict[int, int] = dict()
    end: Dict[int, int] = dict()

    for idx in range(len(dataset)):
        for value in dataset[idx]:
            if value not in counts:
                counts[value] = 1
                start[value] = idx
                end[value] = idx
            else:
                counts[value] += 1
                end[value] = idx


def multi_dict_and_counter(dataset: List[Set[int]], max_value: int) -> None:
    counts = Counter(dataset[0])
    start: Dict[int, int] = dict()
    end: Dict[int, int] = dict()

    for i in range(1, len(dataset)):
        counts.update(dataset[i])

    for idx in range(len(dataset)):
        for value in dataset[idx]:
            if value not in counts:
                start[value] = idx
                end[value] = idx
            else:
                end[value] = idx


class CountAndBoundary:
    def __init__(self, idx: int):
        self.count = 1
        self.start = idx
        self.end = idx

    def add(self, idx: int):
        self.count += 1
        self.end = idx


def class_based(dataset: List[Set[int]], max_value: int) -> None:
    boundaries = dict()

    for idx in range(len(dataset)):
        for value in dataset[idx]:
            if value not in boundaries:
                boundaries[value] = CountAndBoundary(idx)
            else:
                boundaries[value].add(idx)


def list_based(dataset: List[Set[int]], max_value: int) -> None:
    counts = [0 for _ in range(max_value)]
    start = [0 for _ in range(max_value)]
    end = [0 for _ in range(max_value)]

    for idx in range(len(dataset)):
        for value in dataset[idx]:
            counts[value] += 1
            end[value] = idx
            if start[value] == 0:
                start[value] = idx


def numpy_array_based(dataset: List[Set[int]], max_value: int) -> None:
    counts = np.zeros(max_value, dtype=int)
    start = np.zeros(max_value, dtype=int)
    end = np.zeros(max_value, dtype=int)

    for idx in range(len(dataset)):
        for value in dataset[idx]:
            counts[value] += 1
            end[value] = idx
            if start[value] == 0:
                start[value] = idx


def array_based(dataset: List[Set[int]], max_value: int) -> None:
    empty = [0 for _ in range(max_value)]
    counts = array.array("H", empty)
    start = array.array("H", empty)
    end = array.array("H", empty)

    for idx in range(len(dataset)):
        for value in dataset[idx]:
            counts[value] += 1
            end[value] = idx
            if start[value] == 0:
                start[value] = idx


def ctypes_array_based(dataset: List[Set[int]], max_value: int) -> None:
    empty = [0 for _ in range(max_value)]

    counts = (ctypes.c_int * max_value)(*empty)
    start = (ctypes.c_int * max_value)(*empty)
    end = (ctypes.c_int * max_value)(*empty)

    for idx in range(len(dataset)):
        for value in dataset[idx]:
            counts[value] += 1
            end[value] = idx
            if start[value] == 0:
                start[value] = idx


def run_experiment(fn, dataset: List[Set[int]], n_trials: int, max_value: int) -> float:
    assert type(n_trials) == int and n_trials > 0

    start = time.time()
    for _ in range(n_trials):
        fn(dataset, max_value)

    return time.time() - start


if __name__ == "__main__":

    # Generate a random dataset
    max_value = 3000000
    dataset: List[Set[int]] = generate(
        n_indices=5, max_value=max_value, num_values_per_index=100000
    )

    n_trials = 5
    experiments = [
        {"name": "Multi-dicts", "fn": multi_dicts},
        {"name": "Class-based", "fn": class_based},
        {"name": "List-based", "fn": list_based},
        {"name": "Numpy array-based", "fn": numpy_array_based},
        {"name": "Array-based", "fn": array_based},
        {"name": "Ctypes array-based", "fn": ctypes_array_based},
        {"name": "Multi-dict and counter", "fn": multi_dict_and_counter},
    ]

    longest_name_len = max([len(exp["name"]) for exp in experiments])

    for experiment in experiments:
        time_taken = run_experiment(experiment["fn"], dataset, n_trials, max_value)
        print(f"{experiment['name'].ljust(longest_name_len+1)}: {time_taken} seconds")
