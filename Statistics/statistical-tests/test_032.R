sample_1 <- c(3.84, 2.6, 1.19, 2)
sample_2 <- c(3.97, 2.5, 2.7, 3.36, 2.3)

# p-value = 0.4279 > 0.05 => don't reject null hypothesis that
# distributions are identical
mood.test(sample_1, sample_2, alternative = "two.sided")
