# cython: language_level=3
# distutils: language=c
# distutils: sources = ./metrics/positions.c

from libc.stdint cimport uint8_t, uint32_t

cdef extern from "./metrics/positions.h":
    ctypedef struct EntityPositions:
        uint32_t entity_id
        uint8_t n
        uint8_t *arr
    
    ctypedef struct SparsePositionResults:
        uint32_t n
        EntityPositions *results
        char *error_message

    SparsePositionResults positions(char *str, uint32_t max_entity_id, uint8_t min_count)

    void free_sparse_position_results(SparsePositionResults *sparse_results)

class PyEntityPositions:
    def __init__(self, entity_id, n, pos):
        self.entity_id = entity_id
        self.n = n
        self.pos = pos
    
    def __str__(self):
        return f"(entity ID={self.entity_id}, n={self.n}, pos={self.pos})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other) -> bool:
        if type(other) != PyEntityPositions:
            return False
        
        return self.entity_id == other.entity_id and \
            self.n == other.n and \
            self.pos == other.pos

class PySparsePositionResults:
    def __init__(self, n, error_message):
        self.n = n
        self.error_message = error_message
        self.results = []

    def add_result(self, entity_id, n, pos):
        self.results.append(PyEntityPositions(entity_id, n, pos))

    def __str__(self):
        return f"PySparsePositionResults(n={self.n}, error_message={self.error_message}), results={self.results}"
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other) -> bool:
        if type(other) != PySparsePositionResults:
            return False
        
        return self.n == other.n and \
            self.error_message == other.error_message and \
            self.results == other.results

def calc_positions(s, max_entity_id, min_count):

    # Call out to the C function
    cdef SparsePositionResults res = positions(s, max_entity_id, min_count)

    # Convert the C struct to Python objects
    try:
        output = PySparsePositionResults(res.n, res.error_message.decode())
        for i in range(res.n):
            entity_id = res.results[i].entity_id
            n = res.results[i].n
            pos = list(<uint8_t[:res.results[i].n:1]>res.results[i].arr)
            output.add_result(entity_id, n, pos)
    finally:
            free_sparse_position_results(&res)
            pass

    return output