import random
import pickle
import time
from typing import List, Set
from metrics_compiled_c_arrays import calc_metrics
from metrics_compiled_c_array_hash import calc_metrics_array_hash

from metrics_uncompiled import (
    entities_list_of_pickled_list,
    entities_list_of_pickled_set,
    entities_list_of_strings,
)

from metrics_compiled import (
    entities_list_of_pickled_list_compiled,
    entities_list_of_pickled_set_compiled,
    entities_list_of_strings_compiled,
)

from metrics_compiled_vector import (
    entities_strings_compiled_vector,
    entities_strings_compiled_map,
)


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


def list_of_pickled_list(data: List[Set[int]]) -> List[bytes]:
    """Convert generated data to a list of pickled lists of entity IDs."""

    return [pickle.dumps(list(entity_ids)) for entity_ids in data]


def list_of_pickled_set(data: List[Set[int]]) -> List[bytes]:
    """Convert generated data to a list of pickled sets of entity IDs."""

    return [pickle.dumps(entity_ids) for entity_ids in data]


def list_of_strings(data: List[Set[int]]) -> List[str]:
    """Convert generated data to a list of strings of entity IDs."""

    return [" ".join([str(e) for e in entity_ids]) for entity_ids in data]


def concatenated_string(data: List[Set[int]]) -> str:
    """Convert generated data to a concatenated string."""
    return "|".join([" ".join([str(e) for e in entity_ids]) for entity_ids in data])


if __name__ == "__main__":

    # Generate a random dataset
    num_entities = 1000000
    data = generate(10, num_entities, 100000)

    entities_c = lambda s, mc, ne: calc_metrics(s.encode(), ne, mc)

    n_buckets = 1000
    initial_capacity = 100
    filtered_initial_capacity = 100
    entities_c2 = lambda s, mc, ne: calc_metrics_array_hash(
        s.encode(), n_buckets, initial_capacity, mc, filtered_initial_capacity
    )

    experiments = [
        {
            "name": "Uncompiled, list of pickled lists",
            "converter": list_of_pickled_list,
            "fn": entities_list_of_pickled_list,
        },
        {
            "name": "Uncompiled, list of pickled sets",
            "converter": list_of_pickled_set,
            "fn": entities_list_of_pickled_set,
        },
        {
            "name": "Uncompiled, list of strings",
            "converter": list_of_strings,
            "fn": entities_list_of_strings,
        },
        {
            "name": "Compiled, list of pickled lists",
            "converter": list_of_pickled_list,
            "fn": entities_list_of_pickled_list_compiled,
        },
        {
            "name": "Compiled, list of pickled sets",
            "converter": list_of_pickled_set,
            "fn": entities_list_of_pickled_set_compiled,
        },
        {
            "name": "Compiled, list of strings",
            "converter": list_of_strings,
            "fn": entities_list_of_strings_compiled,
        },
        {
            "name": "Compiled, list of strings, C++ vector",
            "converter": list_of_strings,
            "fn": entities_strings_compiled_vector,
        },
        {
            "name": "Compiled, list of strings, C++ map",
            "converter": list_of_strings,
            "fn": entities_strings_compiled_map,
        },
        {
            "name": "Compiled, single string, pure C implementation",
            "converter": concatenated_string,
            "fn": entities_c,
        },
        {
            "name": "Compiled, single string, pure C implementation, array hash table",
            "converter": concatenated_string,
            "fn": entities_c2,
        },
    ]

    max_length_name = max([len(e["name"]) for e in experiments])

    mean_execution_time = [-1 for _ in range(len(experiments))]

    n_trials_per_experiment = 5
    min_count = 0

    for idx, experiment in enumerate(experiments):

        # Convert the generated dataset to the required form
        data_for_test = experiment["converter"](data)

        # Run the single experiment the required number of times
        timings = [-1 for _ in range(n_trials_per_experiment)]
        for i in range(n_trials_per_experiment):
            start_time = time.time()
            result = experiment["fn"](data_for_test, min_count, num_entities)
            timings[i] = time.time() - start_time

        mean_execution_time[idx] = sum(timings) / n_trials_per_experiment

        print(
            f"{experiment['name'].ljust(max_length_name+1)}: {mean_execution_time[idx]} seconds"
        )
