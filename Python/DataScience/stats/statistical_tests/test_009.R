library(lmtest)

sample1 <- c(3083, 3140, 3218, 3239, 3295, 3374, 3475, 3569, 3597, 3725, 3794, 3959, 4043, 4194)
sample2 <- c(75, 78, 80, 82, 84, 88, 93, 97, 99, 104, 109, 115, 120, 127)
sample3 <- c(5, 8, 0, 2, 4, 8, 3, 7, 9, 10, 10, 15, 12, 12)

par(mfrow = c(3, 1))
plot(sample1)
plot(sample2)
plot(sample3)

data <- cbind(sample1, sample2, sample3)
data

# Create a time-series from the data
data.ts <- ts(data)
data.ts

grangertest(sample1 ~ sample2, order = 1, data = data.ts)

grangertest(sample2 ~ sample1, order = 1, data = data.ts)

# Which came first: the chicken or the egg?
data(ChickEgg)
plot.ts(ChickEgg)
grangertest(egg ~ chicken, order = 3, data = ChickEgg)
grangertest(chicken ~ egg, order = 3, data = ChickEgg)

# Generate two datasets
n <- 11
x1 <- rnorm(n, mean = 2) # x1 leads y1
y1 <- rep(0, n)
for (i in 2:n) {
    y1[i] <- x1[i - 1] + rnorm(1, mean = 0, sd = 0.2)
}
x1 <- x1[2:n]
y1 <- y1[2:n]
data <- cbind(x1, y1)
data.ts <- ts(data)
plot.ts(data.ts)

# p-value ~ 1.0
grangertest(x1 ~ y1, order = 1, data = data.ts)

# Null hypothesis: lagged values of x1 don't explain the variation in y1
# p-value < 0.05, therefore the null hypothesis is rejected
grangertest(y1 ~ x1, order = 1, data = data.ts)
