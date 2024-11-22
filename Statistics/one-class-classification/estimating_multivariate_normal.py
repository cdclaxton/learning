# This script estimates the mean and covariance of a multivariate normal
# (Gaussian) distribution.

from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def random_covariance_matrix(n_dimensions):
    """Generate a random positive semidefinite covariance matrix."""

    assert n_dimensions > 0

    is_positive_semidefinite = False

    while not is_positive_semidefinite:

        # Generate a lower triangular matrix L
        L = np.zeros((n_dimensions, n_dimensions))
        for i in range(0, n_dimensions):
            for j in range(0, n_dimensions):
                if i >= j:
                    L[i,j] = stats.norm.rvs(0, 1)

        # Calculate the matrix Omega = L L'
        Omega = np.matmul(L, L.T)

        # Determine if the matrix Omega is positive semidefinite
        is_positive_semidefinite = np.all(np.linalg.eigvals(Omega) > 0)

    return Omega


if __name__ == '__main__':

    n_dimensions = 2
    n_trials = 100
    n_samples = [10, 25, 50, 100, 500, 1000]

    exp_n_samples = []
    mu_error = []
    cov_error = []

    for _ in range(n_trials):

        # Generate a random mean vector
        mu = stats.norm.rvs(0, 1, n_dimensions)

        # Generate a random covariance matrix
        sigma = random_covariance_matrix(n_dimensions)

        # Generate samples from the multivariate normal distribution
        samples = stats.multivariate_normal.rvs(mean=mu, cov=sigma, size=max(n_samples))
        assert samples.shape[0] == max(n_samples)
        assert samples.shape[1] == n_dimensions

        for idx, n in enumerate(n_samples):

            exp_n_samples.append(n)

            # Select n samples from all samples
            samples_subset = samples[:n,]

            # Calculate the error (L2 norm) between the actual mean and the 
            # estimated mean from the samples
            mu_est = np.mean(samples_subset, axis=0)
            mu_error.append(np.linalg.norm(mu - mu_est, ord=2))

            # Calculate the error (L2 norm) between the actual covariance and that 
            # estimated from the samples
            sigma_est = np.cov(samples_subset.T)
            cov_error.append(np.linalg.norm(sigma - sigma_est, ord=2))

    # Create a dataframe for the calculation of the mean errors
    df = pd.DataFrame({
        'n_samples': exp_n_samples,
        'mu_error': mu_error,
        'cov_error': cov_error,
    })
    means = df.groupby('n_samples').mean()

    # Plot the error as a function of the number of samples
    fig, axs = plt.subplots(1, 2)
    axs[0].plot(exp_n_samples, mu_error, 'o', alpha=0.1)
    axs[0].plot(n_samples, means['mu_error'].values)
    axs[0].set_xlabel('Number of samples')
    axs[0].set_ylabel('Error in the mean')

    axs[1].plot(exp_n_samples, cov_error, 'o', alpha=0.1)
    axs[1].plot(n_samples, means['cov_error'].values)
    axs[1].set_xlabel('Number of samples')
    axs[1].set_ylabel('Error in the covariance')
    plt.show()