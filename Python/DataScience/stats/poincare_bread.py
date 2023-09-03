# Henri Poincare's bread analysis
import matplotlib.pyplot as plt
import numpy as np

from scipy import stats


def mean_weight(mu, sigma, n, num_trials):
    """Returns the mean weight of the heaviest bread."""

    heaviest_weights = np.zeros(num_trials)

    for i in range(num_trials):
        bread_weights = np.random.normal(mu, sigma, n)
        heaviest_weights[i] = max(bread_weights)

    return np.mean(heaviest_weights), np.std(heaviest_weights)


def bread_weights(mu, sigma, n, num_trials):
    """Returns an array of the heaviest loaves when n are baked."""

    weights = np.zeros(num_trials)

    for i in range(num_trials):
        weights[i] = max(np.random.normal(mu, sigma, n))

    return weights


if __name__ == '__main__':

    # Mean and standard deviation of the baker's loaves
    mu = 950
    sigma = 50

    fig, axs = plt.subplots(1, 2)

    # Find the value of n that gives a distribution with a mean of 1000g
    num_trials = 365
    ns = range(1, 20)

    mean_weights = np.zeros(len(ns))
    std_dev_weights = np.zeros(len(ns))

    for i,n in enumerate(ns):
        mean_weights[i], std_dev_weights[i] = mean_weight(mu, sigma, n, num_trials)

    n_chosen = np.argmin(np.abs(mean_weights - 1000))
    
    axs[0].plot(ns, mean_weights)
    axs[0].fill_between(ns, mean_weights + std_dev_weights, \
                        mean_weights - std_dev_weights, alpha=0.2)
    axs[0].set_xlabel('Number of loaves in a batch')
    axs[0].set_ylabel('Mean weight of heaviest')
    axs[0].axvline(n_chosen, color='r')

    # Poincare's bread weights    
    weights = bread_weights(mu, sigma, n_chosen, 365)

    axs[1].hist(weights, bins=50)
    axs[1].set_xlabel('Bread weight')
    axs[1].set_ylabel('Count')
    axs[1].set_title(f"Mean = {np.mean(weights):.2f}g, std = {np.std(weights):.2f}g, skew = {stats.skew(weights):.2f}")
    
    plt.tight_layout()
    plt.show()
