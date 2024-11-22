# This script explores how to perform one-class classification using a Gaussian
# model and characterises its performance.
#
# 

import numpy as np
import random
from scipy import stats


def bernoulli(p):
    """Generator of bernoulli samples."""
    assert 0.0 <= p <= 1.0

    def f():
        return stats.binom.rvs(n=1, p=p)
    
    return f


def uniform(a, b):
    """Generator of samples from a continuous uniform distribution in the range [a,b]."""
    assert a <= b

    def f():
        return stats.uniform.rvs(a, b - a)

    return f

def discrete_uniform(a, b):
    """Generator of samples from a discrete uniform distribution in the range [a,b]."""
    assert a <= b

    def f():
        return random.randint(a, b)


def normal(mu, sigma):
    """Generator of samples from a normal (Gaussian) distribution."""
    assert sigma > 0

    def f():
        return stats.norm.rvs(loc=mu, scale=sigma)

    return f

def categorical(category_to_probability):
    """Generator of samples from a categorical distribution."""
    assert type(category_to_probability) == dict

    names = list(category_to_probability.keys())
    probs = list(category_to_probability.values())

    def f():
        idx = np.where(stats.multinomial.rvs(n=1, p=probs))[0][0]
        return names[idx]

    return f


if __name__ == '__main__':

    # Generate a dataset with different types of features
    feature_generators_high = []
    feature_generators_low = []