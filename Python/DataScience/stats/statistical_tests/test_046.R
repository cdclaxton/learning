# 2 successes in 17,887
# 10 successes in 20,000
# p-value = 0.0421 < 0.05 => reject null hypothesis
poisson.test(c(10, 2), c(20000, 17887),
    alternative = "two.sided", conf.level = 0.95
)
