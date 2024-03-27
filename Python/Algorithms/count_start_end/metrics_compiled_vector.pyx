# cython: language_level=3
# distutils: language=c++

import cython
from cython.cimports.libcpp.vector import vector
from cython.cimports.libcpp.map import map
from typing import Dict, List, Tuple

def entities_strings_compiled_vector(
    data: List[str], min_count: cython.uint, num_entities: cython.uint,
) -> List[int]:

    i: cython.uint

    # Number of times an entity has been seen
    counts: vector[cython.uint]
    counts.reserve(num_entities)  # Allocate memory for 'num_entities' elements

    # Start index of the entity
    starts: vector[cython.uint]
    starts.reserve(num_entities)
    
    # End index of the entity
    ends: vector[cython.uint]
    ends.reserve(num_entities)

    # Extract the entities
    for idx, entities in enumerate(data):
        entities = [int(e) for e in entities.split()]

        for e in entities:
            ends[e] = idx
            if counts[e] == 0:
                starts[e] = idx

            # Increment the count for the entity
            counts[e] += 1

    # Return the entities that have a sufficient count
    result = []
    for i in range(num_entities):
        if counts[i] >= min_count:
            result.append((i, starts[i], ends[i]))

    return result

def entities_strings_compiled_map(
    data: List[str], min_count: cython.uint, num_entities: cython.uint,
) -> List[int]:

    i: cython.uint

    # Number of times an entity has been seen
    counts: map[cython.uint, cython.uint]

    # Start index of the entity
    starts: map[cython.uint, cython.uint]
    
    # End index of the entity
    ends: map[cython.uint, cython.uint]

    # Walk through the input string, breaking it into entities and by index
    for idx, entities in enumerate(data):
        entities = [int(e) for e in entities.split()]

        for e in entities:
            ends[e] = idx
            if counts[e] == 0:
                starts[e] = idx

            # Increment the count for the entity
            counts[e] += 1

    # Return the entities that have a sufficient count
    result = []
    for i in range(num_entities):
        if counts[i] >= min_count:
            result.append((i, starts[i], ends[i]))

    return result