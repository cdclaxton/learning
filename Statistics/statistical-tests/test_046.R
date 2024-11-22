# 2 successes in 17,887
# 10 successes in 20,000
# p-value = 0.0421 < 0.05 => reject null hypothesis
poisson.test(c(10, 2), c(20000, 17887),
    alternative = "two.sided", conf.level = 0.95
)

#         Comparison of Poisson rates

# data:  c(10, 2) time base: c(20000, 17887)
# count1 = 10, expected count1 = 6.3346, p-value = 0.0421
# alternative hypothesis: true rate ratio is not equal to 1
# 95 percent confidence interval:
#   0.9529548 41.9743814
# sample estimates:
# rate ratio 
#    4.47175 
