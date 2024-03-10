# Experiment to explore iterating through a list, a set and a dict
from typing import Dict, List, Set
import numpy as np
import time


def make_set_str(num_values: int) -> Set[str]:
    return {f"{i}" for i in range(num_values)}


def make_set_int(num_values: int) -> Set[int]:
    return {i for i in range(num_values)}


def make_list_str(num_values: int) -> List[str]:
    return [f"{i}" for i in range(num_values)]


def make_list_int(num_values: int) -> List[int]:
    return [i for i in range(num_values)]


def make_dict_str(num_values: int) -> Dict[str, int]:
    return {f"{i}": 1 for i in range(num_values)}


def make_dict_int(num_values: int) -> Dict[int, int]:
    return {i: 1 for i in range(num_values)}


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

    e1 = run_experiment(make_set_str, num_values, num_runs)
    e2 = run_experiment(make_list_str, num_values, num_runs)
    e3 = run_experiment(make_dict_str, num_values, num_runs)

    e4 = run_experiment(make_set_int, num_values, num_runs)
    e5 = run_experiment(make_list_int, num_values, num_runs)
    e6 = run_experiment(make_dict_int, num_values, num_runs)

    print(f"set str vs int:   {e1} vs {e4}")
    print(f"list str vs int:  {e2} vs {e5}")
    print(f"dict str vs int:  {e3} vs {e6}")
