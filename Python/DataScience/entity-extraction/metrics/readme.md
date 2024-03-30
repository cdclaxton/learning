# Metrics

This folder contains C code that is compiled using Cython to efficiently
calculate the metrics for a given entity ID.

To compile and run the tests:

```bash
gcc -o metrics -Wall metrics_test.c metrics.c && ./metrics
```