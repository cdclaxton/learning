# cython: language_level=3
# distutils: language=c
# distutils: sources = ./metrics/metrics.c

from libc.stdlib cimport free

cdef extern from "./metrics/metrics.h":
    ctypedef struct EntitySpan:
        int entity_id
        int count
        int start_index
        int end_index

    ctypedef struct ResultSet:
        int n
        EntitySpan *arr
    
    ResultSet calc(char *str, int max_entity_id, int min_count)

class PyResult:
    def __init__(self, entity_id, count, start_index, end_index):
        self.entityId = entity_id
        self.count = count
        self.startIndex = start_index
        self.endIndex = end_index
    
    def __str__(self):
        return f"EntitySpan(id={self.entity_id}, count={self.count}, start={self.start_index}, end={self.end_index})"

    def __repr__(self):
        return self.__str__()

def calc_metrics(s, max_entity_id, min_count):

    # Call out to the C function
    cdef ResultSet res=calc(s, max_entity_id, min_count)

    # Convert the C struct to Python objects
    try:
        output = []
        for i in range(res.n):
            output.append(PyResult(res.arr[i].entity_id, 
            res.arr[i].count,
            res.arr[i].start_index, 
            res.arr[i].end_index))
    finally:
            free(res.arr)

    return output