# cython: language_level=3
# distutils: language=c
# distutils: sources = ./pure-c-metrics-arrays/metrics.c

from libc.stdlib cimport free

cdef extern from "./pure-c-metrics-arrays/metrics.h":
    ctypedef struct EntitySpan:
        int entityId
        int startIndex
        int endIndex

    ctypedef struct ResultSet:
        int n
        EntitySpan *arr
    
    ResultSet calc(char *str, int maxEntityId, int minCount)

class PyResult:
    def __init__(self, entityId, startIndex, endIndex):
        self.entityId = entityId
        self.startIndex = startIndex
        self.endIndex = endIndex
    
    def __str__(self):
        return f"EntitySpan({self.entityId}, {self.startIndex}, {self.endIndex})"

    def __repr__(self):
        return self.__str__()

def calc_metrics(s, maxEntityId, minCount):

    # Call out to the C function
    cdef ResultSet res=calc(s, maxEntityId, minCount)

    # Convert the C struct to Python objects
    try:
        output = []
        for i in range(res.n):
            output.append(PyResult(res.arr[i].entityId, res.arr[i].startIndex, res.arr[i].endIndex))
    finally:
            free(res.arr)

    return output