# Experiment to explore iterating through a list, a set and a dict
from typing import Dict, List, Set
import numpy as np
import time


def make_set(num_values: int) -> Set[str]:
    s = set()
    for i in range(num_values):
        s.add(f"{i}")
    return s


def make_list(num_values: int) -> List[str]:
    return [f"{i}" for i in range(num_values)]


def make_dict(num_values: int) -> Dict[str, int]:
    return {f"{i}": 1 for i in range(num_values)}


def run_experiment(gen_fn, num_values: int, num_runs: int) -> float:
    times = np.zeros(num_runs)
    for i in range(num_runs):
        data = gen_fn(num_values)

        start = time.time()
        for _ in data:
            pass

        times[i] = time.time() - start

    return float(np.mean(times))


if __name__ == "__main__":
    num_values = 100000
    num_runs = 5

    e1 = run_experiment(make_set, num_values, num_runs)
    e2 = run_experiment(make_list, num_values, num_runs)
    e3 = run_experiment(make_dict, num_values, num_runs)

    print(f"set:  {e1}")
    print(f"list: {e2}")
    print(f"dict: {e3}")