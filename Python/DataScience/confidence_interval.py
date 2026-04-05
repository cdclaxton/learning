import numpy as np

if __name__ == "__main__":
    n_experiments = 10000

    population_mean = 10
    population_std_dev = 3

    n_samples = 50
    n_correct = 0

    for i in range(n_experiments):
        # Generate samples from the population
        samples = np.random.normal(
            loc=population_mean, scale=population_std_dev, size=n_samples
        )
        mu = np.mean(samples)
        s = np.std(samples)

        # Standard error
        se = s / np.sqrt(n_samples)

        # 95% confidence interval
        lower_bound = mu - 1.96 * se
        upper_bound = mu + 1.96 * se

        # Fallacy: A 95% confidence interval doesn't mean there's a 95% chance
        # of the population mean falling within the interval
        believe_mean_in_interval = np.random.uniform(0, 1) < 0.95

        if (
            believe_mean_in_interval and lower_bound < population_mean < upper_bound
        ) or (
            not believe_mean_in_interval
            and (population_mean < lower_bound or population_mean > upper_bound)
        ):
            n_correct += 1

    print(f"Proportion correct: {n_correct / n_experiments}")
