import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF


def bernoulli(p):
    return np.random.binomial(1, p)


def chi_squared(observed, expected):
    return np.sum(np.power(observed - expected, 2) / expected)


def chi_squared_test(observed, expected):
    # Calculate the total deviation
    c = chi_squared(observed, expected)
    print(f"Chi-squared: {c}")

    # Calculate the p-value
    return chi2.sf(c, 3)


def plot_chi_squared_distribution(df):
    x = np.linspace(0, 10, 100)
    plt.plot(x, 1 - chi2.cdf(x, df), "r-", lw=5, alpha=0.6, label="chi2 pdf")
    plt.xlabel(r"$\chi^2$")
    plt.show()


def expected_counts(num_samples, p_0, p_1):
    return (
        np.array(
            [
                [(1 - p_0) * (1 - p_1), (1 - p_0) * p_1],  # (0,0), (0,1)
                [p_0 * (1 - p_1), p_0 * p_1],  # (1,0), (1,1)
            ]
        )
        * num_samples
    )


def monte_carlo_cdf(num_samples, p_0, p_1, num_trials):
    # Expected values
    expected = expected_counts(num_samples, p_0, p_1)

    # Vector of the chi-squared values
    chi_squared_values = np.zeros(num_trials)

    for i in range(num_trials):
        observed = generate_samples(num_samples, p_0, p_1)
        chi_squared_values[i] = chi_squared(observed, expected)

    # Calculate the distribution
    return ECDF(chi_squared_values)


def generate_samples(num_samples, p_0, p_1):
    observed = np.zeros((2, 2))
    for _ in range(num_samples):
        f_0 = bernoulli(p_0)
        f_1 = bernoulli(p_1)

        observed[f_0, f_1] += 1

    return observed


if __name__ == "__main__":
    # Number of samples to generate
    num_samples = 200

    # Probability of each feature occurring
    p_0 = 0.3
    p_1 = 0.8

    # Expected number of occurrences assuming independence
    expected = expected_counts(num_samples, p_0, p_1)

    # Number of occurrences of a given (f_0, f_1)
    observed = generate_samples(num_samples, p_0, p_1)

    print(f"Expected: {expected}")
    print(f"Observed: {observed}")

    # Perform a Chi-squared test
    actual_chi_squared = chi_squared(observed, expected)
    p_value = chi_squared_test(observed, expected)
    print(f"p-value using the chi-squared test: {p_value}")

    # Calculate the CDF of the chi-squared statistic using Monte Carlo
    # simulation
    cdf = monte_carlo_cdf(num_samples, p_0, p_1, 1000)

    # Find the probability of seeing a value as large or larger than the
    # computed chi-squared value
    idx = np.where(cdf.x >= actual_chi_squared)[0][0]
    closest = cdf.x[idx]

    prob_of_value_or_greater = 1.0 - cdf.y[idx]
    print(f"Probability of value of greater: {prob_of_value_or_greater}")

    plt.plot(cdf.x, cdf.y)
    plt.axvline(closest, c="r", linestyle="--")
    plt.axhline(cdf.y[idx], c="r", linestyle="--")
    plt.title(f"Probability of value or greater = {prob_of_value_or_greater:.2f}")
    plt.xlabel("$\chi^2$")
    plt.ylabel("Probability")
    plt.show()

    # plot_chi_squared_distribution(1)
