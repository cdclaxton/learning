import numpy as np

if __name__ == '__main__':

    # Probability distribution of failure vs time index
    d = np.array([0.1, 0.2, 0.3, 0.2, 0.2])

    # Generate samples from the distribution
    n_samples = 10000
    samples = [np.argmax(np.random.multinomial(1, d)) for _ in range(n_samples)]

    # Remove failures prior to the current time index
    current_time = 1
    samples_prior = [s for s in samples if s > current_time]

    p_failure_after_current = np.zeros(len(d))
    for s in samples_prior:
        p_failure_after_current[s] += 1

    # Normalise
    p_failure_after_current = p_failure_after_current / np.sum(p_failure_after_current)

    print(f"Simulated:   {p_failure_after_current}")

    # Calculate the theoretical
    p_failure_theoretical = np.zeros(len(d))
    for i in range(current_time+1, len(d)):
        p_failure_theoretical[i] = d[i] / (1 - sum(d[:(current_time+1)]))

    print(f"Theoretical: {p_failure_theoretical}")
