# Think Stats problem (7.6)
#
# Suspect a customer of a casino has replaced a die with a crooked (biased)
# die. In 60 rolls of the die, the following results were obtained:
#
# 1  2  3  4  5  6
# 8  9 19  6  8 10
#
# Use Monte Carlo simulation to compute the probability of seeing a chi-squared
# value as given by the values above.

import numpy as np
import matplotlib.pyplot as plt

from statsmodels.distributions.empirical_distribution import ECDF

def chi_squared(values):
    expected = np.ones(6) / 6
    observed = np.array(values)

    return np.sum(np.power(observed - expected, 2) / expected)


def monte_carlo(num_trials):
    """Calculate the CDF of the chi-squared statistic using Monte Carlo."""

    chi_squared_results = []
    for _ in range(num_trials):
        values = np.random.multinomial(60, np.ones(6)/6)
        chi_squared_results.append(chi_squared(values))

    # Return a CDF
    return ECDF(chi_squared_results)


if __name__ == '__main__':

    actual = [8, 9, 19, 6, 8, 10]
    actual_chi_squared = chi_squared(actual)
    print(f"Chi-squared value: {actual_chi_squared}")

    # Calculate the CDF of the chi-squared statistic using Monte Carlo 
    # simulation
    cdf = monte_carlo(1000)

    # Find the probability of seeing a value as large or larger than the
    # computed chi-squared value
    idx = np.where(cdf.x >= actual_chi_squared)[0][0]
    closest = cdf.x[idx]

    prob_of_value_or_greater = 1.0 - cdf.y[idx]

    plt.plot(cdf.x, cdf.y)
    plt.axvline(closest, c='r', linestyle="--")
    plt.axhline(cdf.y[idx], c='r', linestyle="--")
    plt.title(f"Probability of value = {prob_of_value_or_greater:.2f}")
    plt.xlabel('Chi-squared')
    plt.ylabel('Probability')
    plt.show()
