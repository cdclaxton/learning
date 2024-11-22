value <- c(2.9, 3.5, 2.8, 2.6, 3.7, 3.9, 2.5, 4.3, 2.7, 2.9, 2.4, 3.8, 1.2, 2.0)
sample_group <- factor(c(rep(1, 5), rep(2, 4), rep(3, 5)))
data <- data.frame(sample_group, value)
data


# p-value = 0.2603 > 0.05 => don't reject null hypothesis
oneway.test(value ~ sample_group, data = data, var.equal = TRUE)
