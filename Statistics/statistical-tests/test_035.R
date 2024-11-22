sample.1 <- c(3.84, 2.6, 1.19, 2.0)
sample.2 <- c(3.97, 2.5, 2.7, 3.36, 2.3)

# p-value = 0.7937 > 0.05 => don't reject null hypothesis
ansari.test(sample.1, sample.2, alternative = "two.sided")
