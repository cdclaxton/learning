sample <- c(
    -1.441, -0.642, 0.243, 0.154, -0.325, -0.316,
    0.337, -0.028, 1.359, -1.67, -0.42, 1.02, -1.15,
    0.69, -1.18, 2.22, 1, -1.83, 0.01, -0.77, -0.75,
    -1.55, -1.44, 0.58, 0.16
)

# Test against a normal distribution
# p-value = 0.5351 > 0.05 => don't reject the null hypothesis
# that the data is normally distributed
ks.test(sample, "pnorm")
