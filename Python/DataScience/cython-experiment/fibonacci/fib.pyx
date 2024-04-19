def fib(n):
    """Returns the Fibonacci series up to n."""
    a, b = 0, 1
    result = []
    while b < n:
        result.append(b)
        a, b = b, a + b

    return result