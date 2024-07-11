# Metropolis algorithm with a complex PDF

library(ggplot2)

pdf <- function(x, a, b) {
  
  # Piece-wise PDF
  if (x < 0) 0
  else if (x < 0.5) a + sin(4*pi*x)
  else if (x < 0.75) a
  else if (x < 1) 4*(b-a)*(x-1) + b
  else 0
}

# Plot the PDF
a <- 8/9
b <- 16/9
x <- seq(-0.5, 1.5, 0.01)
y <- sapply(x, function(xi) pdf(xi, a, b))
plot(x,y,'o')

# Generate samples from the complex PDF using the Metropolis algorithm
N <- 100000      # number of samples to draw
x <- rep(NA, N)  # vector for storing the samples
x[1] <- 0.5      # starting value

for (i in 2:N) {
  
  # Proposal function: Gaussian centred at x[i-1] with a std. dev. of 0.05
  # x.c = proposal x
  x.c <- rnorm(1, x[i-1], 0.05)
  
  # Get the probability of the proposal sample and the previous sample
  p.c <- pdf(x.c, a, b)     # pdf of the proposal point
  p.p <- pdf(x[i-1], a, b)  # pdf of the previous point
  
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
  geom_histogram(aes(x = x, y = ..density..), bins = 100)
