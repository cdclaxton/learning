# observed = number of observed events
# expected = number of expected events from a Poisson distribution

# p-value = 1 > 0.05 => don't reject null hypothesis
poisson.test(x = 6, r = 6.22, alternative = "two.sided", conf.level = 0.95)
