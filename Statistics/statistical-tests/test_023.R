library(BSDA)

initial_value <- c(1.83, 0.50, 1.62, 2.48, 1.68, 1.88, 1.55, 3.06, 1.30)
final_value <- c(0.878, 0.647, 0.598, 2.05, 1.06, 1.29, 1.06, 3.14, 1.29)

# p-value = 0.1797 > 0.05 => don't reject the null hypothesis
SIGN.test(initial_value, final_value, alternative = "two.sided")
