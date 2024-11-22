x <- c(59.3, 14.2, 32.9, 69.1, 23.1, 79.3, 51.9, 39.2, 41.8)

# null hypothesis: median = 40
# alternative hypothesis: median != 40
# p-value = 0.50 > 0.05 => don't reject null hypothesis that median = 40
wilcox.test(x, mu = 40, alternative = "two.sided")
