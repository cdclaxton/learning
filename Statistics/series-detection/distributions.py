import math
import numpy as np
import random
from scipy import stats


def beta(alpha, beta):
    """Generator of samples from a beta distribution."""

    assert alpha > 0
    assert beta > 0

    def f():
        return stats.beta.rvs(alpha, beta)

    return f


def bernoulli(p):
    """Generator of bernoulli samples."""
    assert 0.0 <= p <= 1.0

    def f():
        return stats.binom.rvs(n=1, p=p)

    return f


def poisson(mu):
    """Generator of Poisson samples."""
    assert mu >= 0

    def f():
        return stats.poisson.rvs(mu)

    return f


def discrete_uniform(a, b):
    """Generator of samples from a discrete uniform distribution in the range [a,b]."""
    assert a <= b

    def f():
        return random.randint(a, b)

    return f


def continuous_uniform(a, b):
    """Generator of samples from a continuous uniform distribution in the range [a,b]."""
    assert a < b

    def f():
        return stats.uniform.rvs(a, b - a)

    return f


def continuous_uniform_pair(a1, b1, a2, b2):
    """Pair of continuous uniform distribution generators."""
    assert a1 < b1
    assert a2 < b2

    f1 = continuous_uniform(a1, b1)
    f2 = continuous_uniform(a2, b2)

    def f():
        return (f1(), f2())

    return f


def multivariate_normal(sigma):
    """Generator of samples from a symmetric zero-mean multivariate normal distribution."""
    assert type(sigma) == float and sigma > 0

    mu = [0.0, 0.0]
    cov = [[math.pow(sigma, 2), 0.0], [0.0, math.pow(sigma, 2)]]

    def f():
        return stats.multivariate_normal.rvs(mu, cov)

    return f


def categorical(category_to_probability):
    """Generator of samples from a categorical distribution."""
    assert type(category_to_probability) == dict

    names = list(category_to_probability.keys())
    probabilities = list(category_to_probability.values())

    def f():
        idx = np.where(stats.multinomial.rvs(n=1, p=probabilities) == 1)[0][0]
        return names[idx]

    return f
