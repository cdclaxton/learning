# Patients who receive each of three types of drug treatment, A, B and C
tx_A <- c(30, 35, 25, 15, 9)
tx_B <- c(27, 30, 30, 15, 12)
tx_C <- c(20, 28, 20, 12, 7)

data <- data.frame(list(A = tx_A, B = tx_B, C = tx_C))
data

# Variances of the differences
var(data$A - data$B) # 17 -- appears to be an outlier
var(data$A - data$C) # 10.3
var(data$B - data$C) # 10.3

# p-value = 0.8157 > 0.05 => don't reject null hypothesis
mauchly.test(lm(as.matrix(data) ~ 1), X = ~1)
