from setuptools import setup
from Cython.Build import cythonize

# Run: python setup.py build_ext --inplace
setup(
    ext_modules=cythonize(
        [
            "metrics_compiled.pyx",
            "metrics_compiled_vector.pyx",
            "metrics_compiled_c_arrays.pyx",
            "metrics_compiled_c_array_hash.pyx",
        ],
        annotate=True,
    )
)
