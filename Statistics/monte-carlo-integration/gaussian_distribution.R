# Monte Carlo integration of Gaussian distribution

a <- 7   # lower bound
b <- 8  # upper bound
mu <- 6  # mean
sigma <- 1 # sd

# Estimate the area under the curve between a and b
area <- pnorm(b, mu, sigma) - pnorm(a, mu, sigma)

# Estimate using Monte Carlo integration
N <- 10000
m <- 20
x <- runif(N, -m, m)
d <- sapply(x, function(r) {
  if (a <= r & r <= b) dnorm(r, mu, sigma) else 0
})
area.mc <- (2*m / N) * sum(d)

cat("area using pnorm: ", area, "\n")
cat("area using Monte Carlo integration: ", area.mc, "\n")