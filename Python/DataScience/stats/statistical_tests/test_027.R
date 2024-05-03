y <- c(-82.29, -31.14, 136.58, 85.42, 42.96, -122.72, 0.59, 55.77, 117.62, -10.95, -211.38, -304.02, 30.72, 238.19, 140.98, 18.88, -48.21, -63.7)

plot(y)

# p-value = 0.05856 > 0.05 => accept null hypothesis of randomness
lawstat::bartels.test(y, alternative = "two.sided")

# p-value = 0.02928 < 0.05 => reject the null hypothesis
lawstat::bartels.test(y, alternative = "positive.correlated")

# p-value = 0.9707 > 0.05 => accept null hypothesis of randomness
lawstat::bartels.test(y, alternative = "negative.correlated")
