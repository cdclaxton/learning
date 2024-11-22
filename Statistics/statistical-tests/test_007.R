library(psych)

# Generate correlated data
set.seed(1234)
n <- 1000
y1 <- rnorm(n)
y2 <- rnorm(n)
y3 <- y1 + y2 # y3 is dependent on y1 and y2
data <- matrix(c(y1, y2, y3), nrow = n, ncol = 3, byrow = TRUE)

correlation.matrix <- cor(data)
correlation.matrix

# p-value = 0.02 < 0.05 => reject null hypothesis
cortest.bartlett(correlation.matrix, n)
