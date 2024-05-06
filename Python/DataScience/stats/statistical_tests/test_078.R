library(outliers)

sample <- c(0.189, 0.167, 0.187, 0.183, 0.186, 0.182, 0.181, 0.184, 0.177)

# p-value = 0.03868
# Alternative hypothesis: 0.167 is an outlier
grubbs.test(sample, type = 10, opposite = FALSE, two.sided = TRUE)
