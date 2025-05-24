import ctypes
import os

lib_name = "/libsum.so"
_sum = ctypes.CDLL(os.getcwd() + lib_name)

# int calcSum(int length, int *values)
_sum.calcSum.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_int))


class Dataset(ctypes.Structure):
    _fields_ = [
        ("length", ctypes.c_int),  # int length
        ("values", ctypes.POINTER(ctypes.c_double)),  # double *values
    ]


# Dataset *makeDataset(int length)
_sum.makeDataset.argtypes = (ctypes.c_int,)
_sum.makeDataset.restype = ctypes.c_void_p


def calc_sum_using_C(numbers):
    global _sum
    num_numbers = len(numbers)
    array_type = ctypes.c_int * num_numbers
    result = _sum.calcSum(ctypes.c_int(num_numbers), array_type(*numbers))
    return int(result)


if __name__ == "__main__":
    print(calc_sum_using_C([1, 2, 3, 4]))

    # Build a random dataset using the C code
    result = _sum.makeDataset(ctypes.c_int(3))

    d = Dataset.from_address(_sum.makeDataset(ctypes.c_int(2)))
    print(d.length)
    for i in range(d.length):
        print(d.values[i])

    _sum.freeDataset(ctypes.byref(d))
