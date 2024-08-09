library(ADGofTest)

sample <- c(
    -1.441, -0.642, 0.243, 0.154, -0.325, -0.316,
    0.337, -0.028, 1.359, -1.67, -0.42, 1.02, -1.15,
    0.69, -1.18, 2.22, 1, -1.83, 0.01, -0.77, -0.75,
    -1.55, -1.44, 0.58, 0.16
)

# Is the data from a log-normal distribution?
# p-value = 2.4e-05 < 0.05 => reject null hypothesis.
ad.test(sample, plnorm)

# Is the data from a normal distribution?
# p-value = 0.3485 > 0.05 => don't reject null hypothesis.
ad.test(sample, pnorm)
