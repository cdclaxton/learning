# Inference on a Bayesian network using Monte Carlo integration
#
#   e <-- theta  (Bernoulli)  [type of observation]
#   |
#   v
#   t <-- a1,b1 (Uniform)  [observation time if e = 0] (no event)
#     <-- a2,b2 (Uniform)  [observation time if e = 1] (event)
#   |
#   v
#   n <-- sigma  (Gaussian, mu = 0) [measurement noise]
#
# Problem: Given a sample from n, what is the probability of e?

library(ggplot2)

indicator <- function(t, a, b) {
  if (a <= t & t <= b) 1 else 0
}

calc.prob.e <- function(n, theta, a1, b1, a2, b2, sigma) {
  # Estimate the probability that the observation at time is due to an event.
  #
  # Args:
  #   n: Time of the observation.
  #   theta: Probability of an event.
  #   a1: Start time.
  #   b1: End time.
  #   a2: Start time of the event.
  #   b2: End time of the event.
  #   sigma: Standard deviation of the Gaussian measurement noise.
  #
  # Returns:
  #   Estimate of e.
  
  # Preconditions
  stopifnot(0 <= theta & theta <= 1)
  stopifnot(a1 < b1)
  stopifnot(a2 < b2)
  stopifnot(sigma > 0)
  stopifnot(min(a1,a2) <= n)
  stopifnot(max(b1,b2) >= n)
  
  # Perform Monte carlo integration
  n.samples <- 1000
  num.total <- 0
  den.total <- 0
  
  for (i in 1:n.samples) {
  
    t <- runif(1, a1, b1)
    
    num <- (1/(sqrt(2*pi)*sigma)) * (theta / (b2 - a2)) *
      indicator(t, a2, b2) * exp(-0.5 * (n-t)^2 / (sigma^2))
    
    den <- ((1/(sqrt(2*pi)*sigma)) * ((1 - theta) / (b1 - a1)) * 
      indicator(t, a1, b1) * exp(-0.5 * (n-t)^2 / (sigma^2))) + num
    
    num.total <- num.total + num
    den.total <- den.total + den
  }
  
  return(num.total / den.total)
}

theoretical.prob.e <- function(n, theta, a1, b1, a2, b2, sigma) {
  n0 <- pnorm(b2, mean = n, sd = sigma) - pnorm(a2, mean = n, sd = sigma)
  n1 <- pnorm(b1, mean = n, sd = sigma) - pnorm(a1, mean = n, sd = sigma)
  
  e0 <- (theta / (b2-a2)) * n0
  e1 <- ((1-theta) / (b1-a1)) * n1
  
  return(e0 / (e0 + e1))
}

theta <- 0.8
a1 <- 0
b1 <- 100
a2 <- 38
b2 <- 43
sigma <- 3

n.values <- seq(a1, b1, by = 0.2)
df <- data.frame(n = n.values)
df$prob.e <- apply(df, 1, function(r) calc.prob.e(r['n'], theta, a1, b1, a2, b2, sigma))
df$theoretical <- apply(df, 1, function(r) theoretical.prob.e(r['n'], theta, a1, b1, a2, b2, sigma))

ggplot() + 
  geom_point(data = df, mapping = aes(x = n.values, y = prob.e), col = "blue" ) +
  geom_line(data = df, mapping = aes(x = n.values, y = theoretical)) +
  geom_vline(xintercept = a2, col = "red") +
  geom_vline(xintercept = b2, col = "red") +
  xlab("Time of observation") + 
  ylab("Probability observation was due to an event")

