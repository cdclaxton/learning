echo "Python only"
python -m timeit -s "from prime_python import primes" "primes(1000)"

echo "Python compiled"
python -m timeit -s "from prime_compiled import primes" "primes(1000)"

echo "Cython"
python -m timeit -s "from prime import primes" "primes(1000)"