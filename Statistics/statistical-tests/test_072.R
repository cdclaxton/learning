library(fBasics)

sample1 <- c(-2.12, 0.08, -1.59, -0.15, 0.9, -0.7, -0.22, -0.66, -2.14, 0.65, 1.38, 0.27, 3.33, 0.09, 1.45, 2.43, -0.55, -0.68, -0.62, -1.91, 1.11, 0.43, 0.42, 0.09, 0.76)
sample2 <- c(0.91, 0.89, 0.6, -1.31, 1.07, -0.11, -1.1, -0.83, 0.8, -0.53, 0.3, 1.05, 0.35, 1.73, 0.09, -0.51, -0.95, -0.29, 1.35, 0.51, 0.66, -0.56, -0.04, 1.03, 1.47)

# p-value = 0.9113 > 0.05 => don't reject the null hypothesis
# that the data comes from the same distribution
ks.test(sample1, sample2, alternative = "two.sided")

# Alternative       Two-Sided: 0.9113
ks2Test(sample1, sample2)
