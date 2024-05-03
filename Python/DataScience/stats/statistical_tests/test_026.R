y <- c(1.8, 2.3, 3.5, 4, 5.5, 6.3, 7.2, 8.9, 9.1)

plot(y)

# p-value = 0.01278 < 0.05 => reject null hypothesis of randomness
lawstat::runs.test(y, alternative = "two.sided")

# p-value = 0.006388 < 0.05 => reject null hypothesis of randomness
lawstat::runs.test(y, alternative = "positive.correlated")

# p-value = 0.9936 > 0.05 => accept null hypothesis
lawstat::runs.test(y, alternative = "negative.correlated")
