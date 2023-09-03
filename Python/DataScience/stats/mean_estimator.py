# Mean estimator
#
# This script generates samples from a normal distribution with potential
# outliers. It compares the mean and median as an estimator of the mean of
# the normal distribution.

import matplotlib.pyplot as plt
import numpy as np
import random


def error(estimated, mu):
    return np.power(estimated - mu, 2)


if __name__ == '__main__':

    N = 10             # Number of samples per trial
    mu = 0.0           # Mean of the normal distribution
    sigma = 1.0        # Standard deviation of the normal distribution
    max_outliers = 5   # Maximum number of outliers
    M = 100            # Number of trials
    mu_outlier = 10    # Mean of normal distribution for outliers
    sigma_outlier = 2  # Standard deviation of normal distribution for outliers

    mse_mean = []
    mse_median = []

    outliers = range(max_outliers)
    for idx, num_outliers in enumerate(outliers):

        mse_mean.append(0)
        mse_median.append(0)

        for _ in range(M):

            # Generate N samples from a normal distribution
            samples = np.random.normal(mu, sigma, N)
            
            # Randomly select samples to replace with outliers
            outlier_idx = random.sample(range(N), num_outliers)
            for i in outlier_idx:
                samples[i] = np.random.normal(mu_outlier, sigma_outlier, 1)

            mse_mean[idx] += error(np.mean(samples), mu)
            mse_median[idx] += error(np.median(samples), mu)

        mse_mean[idx] = mse_mean[idx] / M
        mse_median[idx] = mse_median[idx] / M

    plt.scatter(outliers, mse_mean, label="Mean", alpha=0.6)
    plt.scatter(outliers, mse_median, label="Median", alpha=0.6)
    plt.legend()
    plt.xlabel('Number of outliers')
    plt.ylabel('Mean squared error')
    plt.xticks(outliers)
    plt.show()
