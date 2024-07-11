# Mixture model fitting with Expectation Maximisation
# ------------------------------------------------------------------------------

# Clear the workspace
rm(list=ls())

# ------------------------------------------------------------------------------
# Define discrete functions
# ------------------------------------------------------------------------------

# Discrete normal distribution
rdiscNorm <- function(n, mu, sigma) {
  r <- floor(rnorm(n, mean=mu, sd=sigma))
}

ddiscNorm <- function(x, mu, sigma, log=FALSE) {
  d <- pnorm(floor(x)+0.5, mean=mu, sd=sigma) -
    pnorm(floor(x)-0.5, mean=mu, sd=sigma)
  if (log) log(d) else d
}

pdiscNorm <- function(x, mu, sigma, log.p=FALSE) {
  p <- pnorm(floor(x)+0.5, mean=mu, sd=sigma)
  if (log.p) log(p) else p
}

# Discrete uniform distribution
rdiscUnif <- function(n, min, max) {
  sample(min:max, n, replace=TRUE)
}

ddiscUnif <- function(x, min, max, log.p=FALSE) {
  d <- ifelse(x >= min & x <= max & round(x) == x, 1/(max-min+1), 0)
  if (log.p) log(d) else d
}

pdiscUnif <- function(x, min, max, log.p=FALSE) {
  p <- c(rep(NA,length(x)))
  for (i in 1:length(x)) {
    if (x[i] < min) p[i] <- 0
    else if (x[i] > max) p[i] <- 1
    else p[i] <- (floor(x[i])-min+1) / (max - min + 1)
  }
  
  if (log.p) log(p) else p
}

# ------------------------------------------------------------------------------
# Define the mixture model
# ------------------------------------------------------------------------------

mixture.NormUnif.samples <- function(n, g1.mu, g1.sigma, unif.min, unif.max, p) {
  d <- rmultinom(n, 1, p)
  d[1,] <- d[1,] * rdiscNorm(n, g1.mu, g1.sigma)
  d[2,] <- d[2,] * rdiscUnif(n, unif.min, unif.max)
  return(colSums(d))
}

mixture.NormUnif.density <- function(x, g1.mu, g1.sigma, unif.min, unif.max, p) {
  p[1]*ddiscNorm(x, g1.mu, g1.sigma) + p[2]*ddiscUnif(x, unif.min, unif.max)
}

# Generate samples from the mixture model
g1.mu <- 3.0
g1.sigma <- 2.0
unif.min <- 5.0
unif.max <- 15.0
p <- c(0.5, 0.5)

x <- seq(-3,15)
y <- mixture.NormUnif.samples(1000, g1.mu, g1.sigma, unif.min, unif.max, p)
d <- mixture.NormUnif.density(x, g1.mu, g1.sigma, unif.min, unif.max, p)

hist(y,breaks=seq(min(y)-2,max(y)+2)-0.5,freq=F)
lines(x,d,col="red",lwd=2)

# Calculate the probability that the i(th) sample belongs to the j(th) component
# y - observation
# w - weights
calc.gamma <- function(y, w, g1.mu, g1.sigma, unif.min, unif.max) {
  # Get the number of samples (n)
  n <- length(y)
  
  # Number of components
  k <- 2
  
  gamma <- matrix(0, n, k)
  
  for (i in 1:n) {
    gamma[i,1] <- w[1]*ddiscNorm(y[i], g1.mu, g1.sigma)
    gamma[i,2] <- w[2]*ddiscUnif(y[i], unif.min, unif.max)
    
    # Ensure the row can be normalised
    if (is.na(gamma[i,1])) gamma[i,1] <- .Machine$double.eps
    if (is.na(gamma[i,2])) gamma[i,2] <- .Machine$double.eps 
    
    if ((gamma[i,1] == 0) & (gamma[i,2] == 0)) {
      gamma[i,1] <- .Machine$double.eps
      gamma[i,2] <- .Machine$double.eps
    }
    
    # Normalise the row
    total <- sum(gamma[i,])
    gamma[i,] <- gamma[i,] / total
  }
  
  return(gamma)
}

# Function to ensure the log of a value can be taken
safe.log <- function(x) {
  if (is.na(x)) { x <- .Machine$double.eps }
  else if (x == 0) { x <- .Machine$double.eps }
  log(x)
}

# Constructor function for M step in EM
make.Mstep.func <- function(y,gamma,w) {
  
  # Get the number of samples
  n <- length(y)
  
  function (p) {
    
    # Extract the parameters from the input vector
    g1.mu <- p[1]
    g1.sigma <- p[2]
    unif.min <- p[3]
    unif.max <- p[4]
    
    total <- 0
    for (i in 1:n) {
      c1 <- w[1]*ddiscNorm(y[i], g1.mu, g1.sigma)
      c2 <- w[2]*ddiscUnif(y[i], unif.min, unif.max)
      
      #print(paste("c1: ", c1))
      #print(paste("c2: ", c2))
      
      total <- total + 
        gamma[i,1] * safe.log(c1) +
        gamma[i,2] * safe.log(c2)
      
    }
    
    print(paste("total:", total))
    return(-total)
  }
}

# Set the initial parameters
g1.mu.m <- 3.0
g1.sigma.m <- 1.0
unif.min.m <- 2.0
unif.max.m <- 10.0
w.m <- c(0.5, 0.5)

# Set the bounds
lower.bound <- c(0.0, 1e-3, 2.0, 18.0)
upper.bound <- c(10.0, 10.0, 15.0, 20.0)

q <- c(0,1)

# Perform EM to find the parameters of the mixture model
iteration.number <- 1

while (abs(q[2] - q[1]) > 1e-3) {
  
  print(paste0("Iteration: ", iteration.number),quote=F)
  
  # Perform the E step
  gamma.m <- calc.gamma(y, w.m, g1.mu.m, g1.sigma.m, unif.min.m, unif.max.m)
  
  # Check that the gamma matrix is well-formed
  if (TRUE %in% is.na(gamma.m)) {
    print("Error: gamma matrix contains NA")
  }
  
  # Calculate the new weight vector
  n_j.m <- colSums(gamma.m)
  w.m <- n_j.m / sum(n_j.m)
 
  # Perform the M step
  fit <- optim(c(g1.mu.m, g1.sigma.m, unif.min.m, unif.max.m), 
               make.Mstep.func(y, gamma.m, w.m),
               method="L-BFGS-B",
               hessian=FALSE,
               lower=lower.bound,
               upper=upper.bound)
   
  g1.mu.m <- fit$par["g1.mu.m"]
  g1.sigma.m <- fit$par["g1.sigma.m"]
  unif.min.m <- fit$par["unif.min.m"]
  unif.max.m <- fit$par["unif.max.m"]
  
  q[1] <- q[2]
  q[2] <- fit$value  
  
  iteration.number <- iteration.number + 1
}










