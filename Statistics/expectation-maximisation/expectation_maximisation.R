# GMM - Expectation Maximisation
# ------------------------------------------------------------------------------

GMM.samples <- function(n, mu, sigma, p) {
  r <- c(rep(0,n))
  for (i in 1:n) {
    j <- rmultinom(1,1,p)
    for (k in 1:length(p)) {
      r[i] <- r[i] + j[k]*rnorm(1,mu[k],sigma[k])
    }
  }
  
  return(r)
}

GMM.density <- function(x, mu, sigma, p) {
  k <- length(p)  # Number of components
  d <- c(rep(0,length(x)))
  
  for (i in 1:length(x)) {
    for (j in 1:k) {
      d[i] <- d[i] + p[j] * dnorm(x[i], mu[j], sigma[j])
    }
  }
  
  return(d)
}
  
# Generate data
n = 1000
mu = c(5,15)
sigma = c(1,2)
p = c(0.3,0.7)
k = length(p)

y <- GMM.samples(n, mu, sigma, p)
hist(y, breaks=50, freq=FALSE, main="Gaussian Mixture Model")

# Plot the density of the GMM
x <- seq(-10,20,0.1)
density <- GMM.density(x, mu, sigma, p)
lines(x, density, col="green", lwd=2)

# Use EM to fit a Gaussian Mixture Model to the data
# ------------------------------------------------------------------------------

# Calculate the probability that the i(th) sample belongs to the j(th) component
calc.gamma <- function(y, w, mu, sigma) {
  # Get the number of components (k) and the number of samples (n)
  k <- length(mu)
  n <- length(y)
  
  gamma <- matrix(0, length(y), k)
  
  for (i in 1:n) {
    for (j in 1:k) {
      gamma[i,j] <- w[j] * dnorm(y[i], mu[j], sigma[j])
    }
    
    # Normalise the row
    total <- sum(gamma[i,])
    gamma[i,] <- gamma[i,] / total
  }
  
  return(gamma)
}

# Constructor function for M step in EM
make.Mstep.func <- function(y,gamma,w) {
  
  # Get the number of samples
  n <- length(y)
  
  # Number of components (k)
  k <- length(w)
  
  function (p) {

    # Extract the mu,sigma parameters from the input vector
    mu <- p[1:k]
    sigma <- p[(k+1):(2*k)]
    
    total <- 0
    for (i in 1:n) {
      for (j in 1:k) {
        l <- w[j]*dnorm(y[i], mu[j], sigma[j])
        if (is.na(l)) l <- .Machine$double.eps
        if (l == 0) l <- .Machine$double.eps
        total <- total + gamma[i,j] * log(l)
      }
    }
    
    #print(-total)
    return(-total)
  }
}

# Initial values of the parameters
w_m <- c(0.5, 0.5)
mu_m <- c(3,9)
sigma_m <- c(0.5, 0.5)

q <- c(0,1)

mu.min <- 0
mu.max <- 20
sigma.min <- 0.1
sigma.max <- 4

iteration.number <- 1

while (abs(q[2] - q[1]) > 1e-3) {

  print(paste0("Iteration: ", iteration.number),quote=F)
  
  gamma_m <- calc.gamma(y, w_m, mu_m, sigma_m)
  
  # Calculate the new weights
  n_j_m <- colSums(gamma_m)
  w_m <- n_j_m / sum(n_j_m)
  
  # Perform the M step
  m <- make.Mstep.func(y, gamma_m, w_m)
  fit <- optim(c(mu_m, sigma_m), m, method="L-BFGS-B",
               lower=c(rep(mu.min,k), rep(sigma.min,k)),
               upper=c(rep(mu.max,k), rep(sigma.max,k)))
  
  print(fit$par)
  print(k)
  mu_m <- fit$par[1:k]
  sigma_m <- fit$par[(k+1):(2*k)]
  
  q[1] <- q[2]
  q[2] <- fit$value
  print("q: ")
  print(q)
  
  print("mu: ")
  print(mu_m)
  
  print("sigma: ")
  print(sigma_m)
  
  # Plot the density of the GMM
  hist(y, breaks=50, freq=FALSE, 
       main=paste0("Gaussian Mixture Model (Iteration ", iteration.number, ")"))
  
  x <- seq(-10,20,0.1)
  density.groundtruth <- GMM.density(x, mu, sigma, p)
  density.GMM <- GMM.density(x, mu_m, sigma_m, w_m)
  lines(x, density.groundtruth, col="green", lwd=2)
  lines(x, density.GMM, col="red", lwd=2)
  
  iteration.number <- iteration.number + 1
}





