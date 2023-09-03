# Central limit theorem
#
# 

import matplotlib.pyplot as plt
import numpy as np


def pdf(x):
    """Probability density function for the piecewise PDF."""

    if x < 0.2:
        return 0.0
    elif 0.2 <= x < 0.4:
        return 1.0
    elif 0.4 <= x < 0.6:
        return 3 - 5*x
    elif 0.6 <= x < 0.8:
        return 3.5
    
    return 0.0

def cdf(x_min, x_max, delta_x):
    """Numerical approximation to cumulative distribution function for the PDF."""

    assert x_min < x_max

    x_vals = [x_min]
    cumulative = [pdf(x_min)]

    for x in np.arange(x_min+delta_x, x_max+delta_x, delta_x):
        x_vals.append(x)
        cumulative.append(pdf(x) + cumulative[-1])

    cumulative = np.array(cumulative)
    cumulative = cumulative / cumulative[-1]

    return x_vals, cumulative

def sample(cdf_x_vals, cumulative, n_samples):
    """Draw a sample from the distribution."""

    assert n_samples > 0

    samples = np.zeros(n_samples)

    for i in range(n_samples):
        u = np.random.uniform(0, 1)
        closest_idx = np.argmin(abs(cumulative - u))
        samples[i] = cdf_x_vals[closest_idx]

    return samples

def samples_of_sum(cdf_x_vals, cumulative, n_trials, n):
    """Samples of the sum of n values."""

    totals = np.zeros(n_trials)

    for i in range(n_trials):
        totals[i] = np.sum(sample(cdf_x_vals, cumulative, n))

    return totals


if __name__ == '__main__':

    fig, axs = plt.subplots(2,2)

    # Plot the PDF
    x = np.arange(0, 1, 0.01)
    f = [pdf(xi) for xi in x]
    axs[0][0].plot(x,f)
    axs[0][0].set_xlabel('x')
    axs[0][0].set_ylabel('Probability')
    axs[0][0].set_title('PDF')
    axs[0][0].set_xlim(0, 1)

    # Plot the CDF
    x_vals, cumulative = cdf(0, 1, 0.001)
    axs[0][1].plot(x_vals, cumulative)
    axs[0][1].set_xlabel('x')
    axs[0][1].set_ylabel('Probability')
    axs[0][1].set_title('CDF') 
    axs[0][1].set_xlim(0, 1)

    # Generate samples from the PDF
    s = sample(x_vals, cumulative, 10000)
    axs[1][0].hist(s, bins=100)
    axs[1][0].set_xlabel('x')
    axs[1][0].set_ylabel('Count')
    axs[1][0].set_title('Histogram of samples')
    axs[1][0].set_xlim(0, 1)

    # Distribution of the sum of n values from the PDF
    totals = samples_of_sum(x_vals, cumulative, 1000, 20)
    axs[1][1].hist(totals, bins=100)
    axs[1][1].set_xlabel('x')
    axs[1][1].set_ylabel('Count')
    axs[1][1].set_title('Histogram of sum of samples')     

    plt.tight_layout()    
    plt.show()
