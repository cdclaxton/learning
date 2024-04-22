import numpy as np
from scipy import stats

x = np.array([44.4, 45.9, 41.9, 53.3, 44.7, 44.1, 50.7, 45.2, 60.1])
y = np.array([2.6, 3.1, 2.5, 5.0, 3.6, 4.0, 5.2, 2.8, 3.8])

statistic, p_value = stats.pearsonr(x, y, alternative="two-sided")

print(f"p-value: {p_value}")
