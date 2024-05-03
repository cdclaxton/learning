library(psych)

# Generate the first dataset with a strong correlation
set.seed(1234)
n <- 100
x1 <- rnorm(n = n, mean = 2, sd = 1)
y1 <- x1 + rnorm(n = n, mean = 0.2, sd = 0.1)
c1 <- cor(matrix(c(x1, y1), nrow = n, ncol = 2, byrow = FALSE))

# Generate the second dataset with very weak correlation
x2 <- rnorm(n = n, mean = 2, sd = 1)
y2 <- rnorm(n = n, mean = 0.2, sd = 0.1)
c2 <- cor(matrix(c(x2, y2), nrow = n, ncol = 2, byrow = FALSE))

# p-value = 2.80e-17 < 0.05 => reject the null hypothesis of equality
# of the correlation matrices
cortest.jennrich(R1 = c1, R2 = c2, n1 = n, n2 = n)
