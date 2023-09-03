# Normal probability plot
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':

    n = 100

    # Generate n samples
    samples = [np.random.normal(2, 0.4) for _ in range(n)]

    fig, axs = plt.subplots(1,2)
    axs[0].hist(samples, bins=20)
    axs[0].set_title("Histogram of samples")

    # Generate rankits
    mu = np.mean(samples)
    sigma = np.std(samples)
    print(f"Estimated mean = {mu}, std. dev = {sigma}")

    num_iterations = 100
    rankits = np.zeros((n, num_iterations))
    for i in range(num_iterations):
        rankits[i] = sorted([np.random.normal(mu, sigma) for _ in range(n)])

    sorted_samples = sorted(samples)
    rankits = np.sum(rankits, axis=0) / num_iterations

    axs[1].plot(rankits, sorted_samples, '.')
    axs[1].set_title('Normal probability plot')
    axs[1].set_xlabel('Rankit')
    axs[1].set_ylabel('Samples')

    plt.tight_layout()
    plt.show()