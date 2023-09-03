# Series of events, which are equally likely to occur at any time
# Measure the times between events = interarrival times

import matplotlib.pyplot as plt
import numpy as np

from statsmodels.distributions.empirical_distribution import ECDF


if __name__ == '__main__':

    max_time = 10
    num_samples = 1000

    # Generate interarrival times
    times = [np.random.uniform(0, max_time) for _ in range(num_samples)]
    times = sorted(times)

    interarrival_times = []
    for i in range(num_samples-1):
        assert times[i+1] >= times[i], f"{times[i+1]}, {times[i]}"
        interarrival_times.append(times[i+1] - times[i])

    lam = max_time / num_samples
    print(f"Mean interarrival time: {np.mean(interarrival_times)}")
    print(f"Expected mean interarrival time: {max_time} / {num_samples} = {lam}")

    # Calculate the empirical CDF
    cdf = ECDF(interarrival_times)
    
    # Plot
    fig, axs = plt.subplots(2,2)

    axs[0][0].hist(interarrival_times, bins=100)
    axs[0][0].set_title('Histogram of interarrival times')
    axs[0][0].set_xlabel('Interarrival time')
    axs[0][0].set_ylabel('Count')

    axs[0][1].hist([np.random.exponential(lam) for _ in range(num_samples)], bins=100)
    axs[0][1].set_title('Histogram of samples from an exponential distribution')
    axs[0][1].set_xlabel('x')
    axs[0][1].set_ylabel('Count')    
   
    axs[1][0].plot(cdf.x, cdf.y)
    axs[1][0].set_title('Empirical CDF')
    axs[1][0].set_xlabel('Interarrival time')
    axs[1][0].set_ylabel('Probability')

    axs[1][1].plot(cdf.x, 1 - cdf.y)
    axs[1][1].set_yscale('log')
    axs[1][1].set_title('Log of the CDF of interarrival times')
    axs[1][1].set_xlabel('Interarrival time')
    axs[1][1].set_ylabel('1 - probability')

    plt.tight_layout()
    plt.show()
