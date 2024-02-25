import numpy as np
import random
import time
from BTrees.UUBTree import UUBTree


def generate_dataset():
    data = []
    for i in range(100000):
        data.extend([i for _ in range(random.randint(0, 5))])

    random.shuffle(data)
    return data


def experiment_dict(data):
    d = dict()
    for value in data:
        if value not in d:
            d[value] = 1
        else:
            d[value] += 1


def experiment_dict2(data):
    d = dict()
    for value in data:
        d[value] = d.get(value, 0) + 1


def experiment_btree(data):
    t = UUBTree()
    for value in data:
        if value not in t:
            t.update({value: 1})
        else:
            t.update({value: t[value] + 1})


def run_experiment(experiment, data, num_runs):
    times = np.zeros(num_runs)
    for i in range(num_runs):
        start = time.time()
        experiment(data)
        times[i] = time.time() - start

    return np.mean(times)


if __name__ == "__main__":
    data = generate_dataset()
    num_runs = 5

    print(f"Number of elements: {len(data)}")
    print(f"dict:   {run_experiment(experiment_dict, data, num_runs)}")
    print(f"dict2:  {run_experiment(experiment_dict2, data, num_runs)}")
    print(f"b-tree: {run_experiment(experiment_btree, data, num_runs)}")
