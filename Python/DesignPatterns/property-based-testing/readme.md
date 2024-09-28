# Property-based testing

## Setup

```bash
# Install the required dependencies
pip install -r requirements.txt

# Run the tests
pytest .

# Run the tests and see detailed information
pytest --hypothesis-show-statistics .
```

## Properties to test

Examples from: https://fsharpforfunandprofit.com/posts/property-based-testing-2/

* Different paths, same destination -- if operations are commutative
* There and back again -- combine an operation with its inverse
* Some things never change -- invariant is preserved after some operation
* Idempotence -- doing an operation twice is the same as doing it once
* Hard to prove, easy to verify
* Test oracle -- alternative implementation, e.g. high performance approach vs. 
    a brute-force approach or a concurrent implementation vs. a single-threaded
    implementation
