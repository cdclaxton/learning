# 2 successes in 17,887
# 10 successes in 20,000
import statsmodels.stats.rates as smr

result = smr.test_poisson_2indep(
    count1=2,
    exposure1=17887,
    count2=10,
    exposure2=20000,
    alternative="two-sided",
    method="exact-cond",  # same as in R
)
print(result)
print(f"p-value: {result.pvalue}")
