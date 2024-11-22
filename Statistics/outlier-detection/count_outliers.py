# Outlier detection in sparse count data

import math
import matplotlib.pyplot as plt
import random
import statsmodels.stats.rates as smr
from scipy import stats


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


def generate_dataset(
    n, p_outlier, outlier_extent, p_sample_given_normal, p_sample_given_outlier
):
    """Generate a dataset of n samples."""

    assert n > 0

    # Generate the initial sample
    outlier_present = [p_outlier() == 1]
    end_idx = outlier_extent() if outlier_present[-1] else None
    samples = [
        p_sample_given_normal() if not outlier_present[-1] else p_sample_given_outlier()
    ]

    for i in range(1, n):
        if end_idx is not None and i < end_idx:
            samples.append(p_sample_given_outlier())
            outlier_present.append(True)
        else:
            outlier_present.append(p_outlier() == 1)
            if outlier_present[-1]:
                end_idx = outlier_extent() + i
                samples.append(p_sample_given_outlier())
            else:
                end_idx = None
                samples.append(p_sample_given_normal())

    return samples, outlier_present


def estimate_outliers(dataset, learn_window, test_window):
    """Estimate the outliers in the dataset."""

    assert type(dataset) == list
    assert type(learn_window) == int and learn_window > 0
    assert type(test_window) == int and test_window > 0

    num_slides = len(dataset) - (learn_window + test_window)
    if num_slides < 0:
        return {}

    result = {}
    for start_index in range(num_slides):
        m = start_index + learn_window
        learn_data = dataset[start_index:m]
        test_data = dataset[m : (m + test_window)]

        assert len(learn_data) == learn_window
        assert len(test_data) == test_window

        # ratio = rate1 / rate2 = (test rate) / (learn rate)
        test_result = smr.test_poisson_2indep(
            count1=test_window,
            exposure1=sum(test_data),
            count2=learn_window,
            exposure2=sum(learn_data),
            alternative="larger",
            method="exact-cond",
        )

        # Store the p-value for the mid point of the test window
        mid_point_test_window = m + math.floor(test_window / 2)
        result[mid_point_test_window] = test_result.pvalue

    return result


if __name__ == "__main__":

    n = 100
    p_outlier = bernoulli(0.05)
    outlier_extent = discrete_uniform(1, 5)
    p_sample_given_normal = poisson(0.1)
    p_sample_given_outlier = poisson(1)

    samples, outlier_present = generate_dataset(
        n, p_outlier, outlier_extent, p_sample_given_normal, p_sample_given_outlier
    )

    learn_window = 10
    test_window = 2
    result = estimate_outliers(samples, learn_window, test_window)
    print(result)

    colours = ["r" if xi else "b" for xi in outlier_present]
    plt.scatter(list(range(n)), samples, c=colours)
    plt.show()
