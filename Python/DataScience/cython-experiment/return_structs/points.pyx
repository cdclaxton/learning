# cython: language_level=3
# distutils: language=c
# distutils: sources = points_src.c

from libc.stdlib cimport free

cdef extern from "points_src.h":
    ctypedef struct Point:
        int x
        int y
    
    ctypedef struct Points:
        int n
        Point *arr

    Points create(int start_x, int start_y, int offset_x, int offset_y, int n)

class PyResult:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

def create_points(start_x, start_y, offset_x, offset_y, n):

    # Call out to the C function
    cdef Points res=create(start_x, start_y, offset_x, offset_y, n)

    # Convert the C struct to Python objects
    try:
        output = []
        for i in range(res.n):
            output.append(PyResult(res.arr[i].x, res.arr[i].y))
    finally:
        free(res.arr)

    return output