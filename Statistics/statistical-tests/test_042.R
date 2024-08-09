# x = number of observed successes
# n = number of trials
# p = hypothesised probability of success
# p-value < 0.05 => reject null hypothesis that p=0.5
binom.test(x = 25, n = 30, p = 0.5, alternative = "two.sided", conf.level = 0.95)

# p-value = 0.0001625 < 0.05 => reject null hypothesis that p=0.5
binom.test(x = 25, n = 30, p = 0.5, alternative = "greater", conf.level = 0.95)
