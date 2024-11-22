values <- c(8, 8, 7, 7, 6, 6, 6, 8, 6, 8, 9, 7, 5, 8, 5, 9, 7, 7, 7, 7, 7, 8, 7, 7, 8, 6, 8, 7, 6, 6, 7, 8, 6, 9, 9, 6)
diet_data <- matrix(values,
    nrow = 12,
    byrow = TRUE,
    dimnames = list(1:12, c("Healthy balanced", "Low fat", "Low carb"))
)
diet_data

# p-value = 0.02237 => reject null hypothesis
friedman.test(diet_data)
