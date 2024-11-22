import matplotlib.pyplot as plt
import numpy as np
import random
from scipy import stats
from statsmodels.distributions.empirical_distribution import ECDF

# Level of agreement between analysts
agreement = [3 / 5, 4 / 5, 5 / 5]

# Proportion of the agreements
proportion = [0.3, 0.6, 0.1]

# Number of pairs of leads reviewed
n_pairs = 20


def uniform(min_value, max_value, n):
    return stats.uniform.rvs(loc=min_value, scale=max_value - min_value, size=n)


def bernoulli(p, n):
    return np.array([1 if random.random() < p else 0 for _ in range(n)])


def multinominal(p):
    x = stats.multinomial.rvs(n=1, p=p, size=1)
    return np.where(x[0] == 1)[0][0]


proportion_system_agreements = []
for _ in range(1000):
    system_agreement = [uniform(0, a, 1)[0] for a in agreement]

    total_system_agreement_with_analysts = 0
    for _ in range(n_pairs):
        idx = multinominal(proportion)
        total_system_agreement_with_analysts += bernoulli(system_agreement[idx], 1)[0]

    proportion_system_agreements.append(total_system_agreement_with_analysts / n_pairs)

# Calculate the empirical CDF
ecdf = ECDF(proportion_system_agreements)
idx = np.argmin(np.abs(ecdf.y - 0.95))
x_value = ecdf.x[idx]

plt.hist(proportion_system_agreements, bins=20, density=True)
plt.axvline(x=x_value, color="r")
plt.xlabel("Proportion of system agreements with analyst consensus")
plt.show()
