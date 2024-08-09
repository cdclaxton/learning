binary_factor <- factor(c(1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0))

# p-value = 0.001 < 0.05 => reject null hypothesis of randomness
tseries::runs.test(binary_factor, alternative = "two.sided")

# alternatives:
# less - under-mixing (clustered)
# greater - over-mixing (scattered)

# p-value = 0.0006811 < 0.05 => reject the null hypothesis in favour of
# the alternative hypothesis that the data is under-mixed
tseries::runs.test(binary_factor, alternative = "less")

# p-value = 0.9993 > 0.05 => don't reject the null hypothesis
tseries::runs.test(binary_factor, alternative = "greater")
