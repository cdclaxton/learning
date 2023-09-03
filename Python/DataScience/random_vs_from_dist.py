# Samples are drawn from a discrete probability distribution that has a finite
# extent, e.g. 7 possible values.

import matplotlib.pyplot as plt
import numpy as np

def calc_error(actual, estimated):
    return np.power(actual - estimated, 2)


if __name__ == '__main__':

    # Generate the random probability distribution
    alpha = np.array([1, 1, 1, 1, 1])
    n = len(alpha)
    p = np.random.dirichlet(alpha)
    print(p)

    # Find the most likely
    most_likely = np.argmax(p)
    print(f"Most likely: {most_likely}")

    mean_index = 0
    for idx, prob in enumerate(p):
        mean_index += (idx * prob)

    error_most_likely = []
    error_mean = []
    error_random = []

    counts = {}

    num_experiments = 10000
    for _ in range(num_experiments):

        # Draw a sample from the distribution
        sample = np.argmax(np.random.multinomial(1, p, 1) == 1)
        if sample not in counts:
            counts[sample] = 1
        else:
            counts[sample] += 1

        # Random sample in the range
        random_sample = np.random.randint(0, n)

        # Calculate the errors
        error_most_likely.append(calc_error(sample, most_likely))
        error_mean.append(calc_error(sample, mean_index))
        error_random.append(calc_error(sample, random_sample))

    print(f"Error most likely: {np.mean(error_most_likely)}")
    print(f"Error mean: {np.mean(error_mean)}")
    print(f"Error random: {np.mean(error_random)}")
    print(f"Counts: {counts}")

    n = len(error_most_likely)
    jitter = 0.1
    plt.plot(np.random.normal(1, jitter, n), error_most_likely, '.', alpha=0.2)
    plt.plot(np.random.normal(2, jitter, n), error_mean, '.', alpha=0.2)
    plt.plot(np.random.normal(3, jitter, n), error_random, '.', alpha=0.2)
    plt.show()