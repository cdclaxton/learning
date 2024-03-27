# cython: language_level=3
# distutils: language=c
# distutils: sources = ./pure-c-metrics-array-hash-table/metrics.c

from libc.stdlib cimport free

cdef extern from "./pure-c-metrics-array-hash-table/metrics.h":
    ctypedef struct Item:
        int entity_id
        int count
        int start_index
        int end_index

    ctypedef struct FilteredItems:
        int n_items
        Item *items

    FilteredItems calc(char *str,
                   int n_buckets,
                   int initial_capacity,
                   int min_count,
                   int filtered_initial_capacity)

class PyResult2:
    def __init__(self, entity_id, count, start_index, end_index):
        self.entity_id = entity_id
        self.count = count
        self.start_index = start_index
        self.end_index = end_index
    
    def __str__(self) -> str:
        return f"Item({self.entity_id}, {self.count}, {self.start_index}, {self.end_index})"

    def __repr__(self) -> str:
        return self.__str__()

def calc_metrics_array_hash(s, n_buckets, initial_capacity, min_count, filtered_initial_capacity):

    # Call out to the C function
    cdef FilteredItems res = calc(s,
                    n_buckets,
                    initial_capacity,
                    min_count,
                    filtered_initial_capacity)

    # Convert the C struct to Python objects
    try:
        output = []
        for i in range(res.n_items):
            output.append(PyResult2(res.items[i].entity_id,
                res.items[i].count,
                res.items[i].start_index,
                res.items[i].end_index ))
    finally:
        free(res.items)
    
    return output