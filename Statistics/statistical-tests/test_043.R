# x = number of observed successes
# n = number of trials
# p = hypothesised probability of success

# 52 heads in 100 coin tosses
# p-value = 0.7642 > 0.05 => don't reject null hypothesis (coin is considered fair)
prop.test(
    x = 52, n = 100, p = 0.5,
    alternative = "two.sided", conf.level = .95
)

# p-value = 0.7644
binom.test(
    x = 52, n = 100, p = 0.5,
    alternative = "two.sided", conf.level = 0.95
)

## H0: The null hypothesis is that the four populations from which
##     the patients were drawn have the same true proportion of smokers.
## A:  The alternative is that this proportion is different in at
##     least one of the populations.
##
## p-value = 0.005585 < 0.05 => reject null hypothesis

smokers <- c(83, 90, 129, 70)
patients <- c(86, 93, 136, 82)
prop.test(smokers, patients)
