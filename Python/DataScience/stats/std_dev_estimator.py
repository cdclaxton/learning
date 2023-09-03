# Standard deviation estimation
#
# This script compares the mean error when using the following two statistics
# for the calculation of the standard deviation:
#
# 1. 1/N \sum (x_i - \bar{x})^2
# 2. 1/(N-1) \sum (x_i - \bar{x})^2
#
# For small numbers of samples, the first statistic is a biased estimator.

import matplotlib.pyplot as plt
import numpy as np


def s_n(x):
    """Compute the standard deviation using 1/N \sum (x_i - \bar{x})^2."""

    N = len(x)
    x_bar = np.mean(x)
    return (1/N) * np.sum(np.power(x - x_bar, 2))


def s_n_minus_1(x):
    """Compute the standard deviation using 1/(N-1) \sum (x_i - \bar{x})^2."""

    N = len(x)
    x_bar = np.mean(x)
    return (1/(N-1)) * np.sum(np.power(x - x_bar, 2))


if __name__ == '__main__':

    mu = 0.0          # Mean of the normal distribution
    sigma = 1.0       # Standard deviation of the normal distribution
    N = 100           # Number of samples to generate
    num_trials = 1000 # Number of trials per number of samples

    num_samples = list(np.arange(2, 50))
    me_s_n = []
    me_s_n_minus_1 = []

    for ns in num_samples:

        errors_s_n = []
        errors_s_n_minus_1 = []

        for trial in range(num_trials):
            
            # Generate the samples
            x = np.random.normal(mu, sigma, ns)

            errors_s_n.append(s_n(x) - sigma)
            errors_s_n_minus_1.append(s_n_minus_1(x) - sigma)

        me_s_n.append(np.sum(errors_s_n) / num_trials)
        me_s_n_minus_1.append(np.sum(errors_s_n_minus_1) / num_trials)

    plt.scatter(num_samples, me_s_n, label='1/N scaling')
    plt.scatter(num_samples, me_s_n_minus_1, label='1/(N-1) scaling')#
    plt.legend()
    plt.axhline(0)
    plt.xlabel('Number of samples')
    plt.ylabel('Mean error')
    plt.title('Mean error of standard deviation')
    plt.show()

