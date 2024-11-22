# The sum of samples from a Poisson distribution is also Poisson distributed.

import numpy as np
from scipy import stats
import statsmodels.stats.rates as smr
import matplotlib.pyplot as plt


if __name__ == "__main__":

    learn_window_size = 90
    test_window_size = 10

    mu_learn = 1
    ratios = np.arange(0.1, 5, 0.1)
    alerting_ratio = 1.5
    number_of_trial_per_ratio = 20

    true_ratios = []
    p_values = []

    for ratio in ratios:
        for _ in range(number_of_trial_per_ratio):

            learn_data = stats.poisson.rvs(mu_learn, size=learn_window_size)
            test_data = stats.poisson.rvs(ratio * mu_learn, size=test_window_size)

            learn_counts = np.sum(learn_data)
            test_counts = np.sum(test_data)

            if learn_counts == 0 or test_counts == 0:
                continue

            test_result = smr.test_poisson_2indep(
                count1=test_counts,
                exposure1=test_window_size,
                count2=learn_counts,
                exposure2=learn_window_size,
                alternative="larger",
                method="exact-cond",
                value=alerting_ratio,
            )

            est_test_ratio = test_counts / test_window_size
            est_learn_ratio = learn_counts / learn_window_size

            true_ratios.append(est_test_ratio / est_learn_ratio)
            p_values.append(test_result.pvalue)

    colours = ["r" if p < 0.05 else "b" for p in p_values]

    plt.scatter(true_ratios, p_values, c=colours, alpha=0.1)
    plt.xlabel("Ratio of rates")
    plt.ylabel("p-value")
    plt.title(f"Alerting ratio of {alerting_ratio}")
    plt.show()
