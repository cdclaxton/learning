import numpy as np

from scipy import stats


def bernoulli(p):
    """Bernoulli distribution where the probability of a 1 is p."""

    dist = stats.bernoulli(p)

    def f():
        return dist.rvs()

    return f


def discrete_uniform(min_value, max_value):
    """Discrete uniform distribution in the range [min_value, max_value]."""
    dist = stats.randint(min_value, max_value + 1)

    def f():
        return dist.rvs()

    return f


def continuous_uniform(min_value, max_value):
    """Continuous uniform distribution in the range [min_value, max_value]."""
    dist = stats.uniform(min_value, max_value - min_value)

    def f():
        return dist.rvs()

    return f


def multinomial(p):
    """Multinomial distribution."""
    dist = stats.multinomial(n=1, p=p)

    def f():
        sample = dist.rvs()[0]
        return np.where(sample == 1)[0][0]

    return f
