library(outliers)

sample <- c(0.189, 0.167, 0.187, 0.183, 0.186, 0.182, 0.181, 0.184, 0.177)

# Perform test on the smallest value
# p-value = 0.1137 > 0.05 => not significant
dixon.test(sample)

# p-value = 0.8924
dixon.test(sample, opposite = TRUE)
