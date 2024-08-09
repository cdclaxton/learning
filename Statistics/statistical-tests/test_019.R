initial_value <- c(16, 20, 21, 22, 23, 22, 27, 25, 27, 28)
final_value <- c(19, 22, 24, 24, 25, 25, 26, 26, 28, 32)

# Null hypothesis: sample means are equal
# p-value = 0.002 < 0.05 => reject null hypothesis
t.test(final_value, initial_value, alternative = "two.sided", paired = TRUE)
