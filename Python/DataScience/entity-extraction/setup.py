from setuptools import setup
from Cython.Build import cythonize

# Run: python setup.py build_ext --inplace
setup(
    ext_modules=cythonize(
        ["metrics_compiled_c_arrays.pyx", "positions_compiled_c.pyx"],
        annotate=True,
    )
)
