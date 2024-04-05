from setuptools import setup
from Cython.Build import cythonize

# Run: python setup.py build_ext --inplace
setup(
    ext_modules=cythonize(
        [
            "positions_compiled_c.pyx",
            "adds_removes.pyx",
        ],
        annotate=True,
    )
)
