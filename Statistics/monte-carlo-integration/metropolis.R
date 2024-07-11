# Metropolis algorithm -- Gaussian distribution

library(ggplot2)

mu <- 2         # mean of the Gaussian distribution
sigma <- 1      # standard deviation of the Gaussian distribution

N <- 500000     # number of samples to draw
x <- rep(0, N)  # vector for storing all of the samples
x[1] <- 0.5     # starting value

# Generate samples
for (i in 2:N) {
  
  # Proposal function: Gaussian centred at x[i-1] with a std. dev. of 0.05
  # x.c = proposal x
  x.c <- rnorm(1, x[i-1], 0.05)
  
  # Get the probability of the proposal sample and the previous sample
  p.c <- dnorm(x.c, mu, sigma)     # pdf of the proposal point
  p.p <- dnorm(x[i-1], mu, sigma)  # pdf of the previous point
  
  # Sample from the uniform distribution
  u <- runif(1, 0, 1)
  
  # Generate the new sample
  if (u < min(1, p.c/p.p)) {
    x[i] <- x.c
  } else {
    x[i] <- x[i-1]
  }
}

# Plot the distribution
ggplot(data.frame(x)) + 
  geom_histogram(aes(x = x, y = ..density..), bins = 100) +
  stat_function(fun = dnorm, 
                args = list(mean = mu, sd = sigma), 
                lwd = 1, 
                col = 'blue')
