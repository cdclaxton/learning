from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(["prime.pyx", "prime_compiled.py"], annotate=True))
