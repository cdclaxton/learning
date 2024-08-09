x <- c(59.3, 14.2, 32.9, 69.1, 23.1, 79.3, 51.9, 39.2, 41.8)

# alternative hypothesis: true mean is not equal to 40
# p-value = 0.45 > 0.05 => don't reject null hypothesis that the mean is 40
t.test(x, mu = 40, alternative = "two.sided", conf.level = 0.95)

# null hypothesis: true mean is < 30
# alternative hypothesis: true mean is > 30
# p-value = 0.03 < 0.05 => reject null hypothesis that true mean is <30
t.test(x, mu = 30, alternative = "greater", conf.level = 0.95)
