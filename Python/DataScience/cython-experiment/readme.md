# Cython

Cython is Python with C data types

`pip install cython`

## Hello World example

```bash
# Build the .so file
python setup.py build_ext --inplace

# Run a script using the compiled code
python run.py
```

## Fibonacci example

```bash
python setup.py build_ext --inplace
python run.py
```

## Prime number example

```bash
cd ./primes
python setup.py build_ext --inplace
python run.py
```

Open `prime.html` in a web browser.