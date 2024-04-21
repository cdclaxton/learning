import numpy as np
from scipy import stats
import statistics
import math

if __name__ == "__main__":
    # Example from https://courses.lumenlearning.com/introstats1/chapter/matched-or-paired-samples/
    before = np.array([6.6, 6.5, 9.0, 10.3, 11.3, 8.1, 6.3, 11.6])
    after = np.array([6.8, 2.4, 7.4, 8.5, 8.1, 6.1, 3.4, 2.0])
    n = len(before)

    diffs = after - before

    # Sample means
    x_bar = statistics.mean(diffs)

    # Sample standard deviation
    s_d = math.sqrt(statistics.variance(diffs))

    # Number of degrees of freedom
    df = n - 1

    # t test statistic
    t = x_bar / (s_d / math.sqrt(n))
    p_value = stats.t.cdf(t, df)
    print(f"p-value: {p_value}")
    alpha = 0.05
    if p_value < alpha:
        print("Reject the null hypothesis that there is no difference")
    else:
        print("Accept the null hypothesis that there is no difference")
