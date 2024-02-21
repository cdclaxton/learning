# Experiment using large dicts
import random
import numpy as np
import time

from collections import defaultdict


def generate_value(num_values: int) -> int:
    return random.randint(0, num_values - 1)


def experiment_dict(max_value: int, num_entries: int) -> None:
    s = dict()
    for _ in range(num_entries):
        value = generate_value(max_value)
        if value not in s:
            s[value] = 1
        else:
            s[value] += 1


def experiment_defaultdict(max_value: int, num_entries: int) -> None:
    s: defaultdict[int, int] = defaultdict(int)
    for _ in range(num_entries):
        value = generate_value(max_value)
        s[value] += 1


def experiment_list(max_value: int, num_entries: int) -> None:
    s = [0 for _ in range(max_value)]
    for _ in range(num_entries):
        s[generate_value(max_value)] += 1


def average_experiment_time(
    experiment, max_value: int, num_entries: int, num_tries: int
) -> float:
    times = np.zeros(num_tries)
    for idx in range(num_tries):
        start = time.time()
        experiment(max_value, num_entries)
        times[idx] = time.time() - start

    return float(np.mean(times))


if __name__ == "__main__":

    max_value = 30000000
    num_entries = 5000
    num_tries = 5

    e1 = average_experiment_time(experiment_dict, max_value, num_entries, num_tries)
    e2 = average_experiment_time(
        experiment_defaultdict, max_value, num_entries, num_tries
    )
    e3 = average_experiment_time(experiment_list, max_value, num_entries, num_tries)

    print(f"dict:        {e1}")
    print(f"defaultdict: {e2}")
    print(f"list:        {e3}")
