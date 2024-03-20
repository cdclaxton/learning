# distutils: language=c
# distutils: sources = point_src.c

cdef extern from "point_src.h":
    cdef struct Point:
        int x
        int y
    Point new_point(int x, int y)

cdef class PyPoint:
    cdef Point p

    def __init__(self, x, y):
        self.p = new_point(x, y)

    def x(self):
        return self.p.x

    def y(self):
        return self.p.y