# Particle Filtering
#
# Adapted from: 
# http://studentdavestutorials.weebly.com/particle-filter-with-matlab-code.html
#
# Quail: Non-linear flight model (with imprecise measurements)
# 1-D model, discrete time steps

# Clear the environment
rm(list=ls())

# Initialise the variables
x.initial <- 0.1       # initial state of the quail
sigma_squared.N <- 1   # noise covariance (state update)
sigma_squared.R <- 1   # noise covariance (measurement)
t <- 75                # duration (number of iterations of the chase)
N <- 100               # number of particles the system generates
V <- 2                 # variance of the initial estimate (of each particle)

# The functions used by the quail are:
# x = 0.5*x + 25*x/(1 + x^2) + 8*cos(1.2*(t-1)) + PROCESS NOISE
#   where PROCESS NOISE ~ N(0, sqrt(x.N))
# z = x^2/20 + MEASUREMENT NOISE
#   where MEASUREMENT NOISE ~ N(0, sqrt(x.R))

update.position <- function(x, t) {
  n <- rnorm(1, 0, sqrt(sigma_squared.N))  # process noise
  return(0.5*x + 25*x/(1 + x^2) + 8*cos(1.2*(t-1)) + n)
}

measurement <- function(x) {
  n <- rnorm(1, 0, sqrt(sigma_squared.R))  # measurement noise
  return(x^2 / 20 + n)
}

obs.prob <- function(z.obs, z) {
  constant <- 1/sqrt(2 * pi * sigma_squared.R)
  k <- (z - z.obs)^2 / (2 * sigma_squared.R)
  return(constant * exp(-k))
}

# Create a vector to hold the position (state) of the quail and then set
# the initial position
x <- c(rep(0,t))
x[1] <- x.initial

# Create a vector to hold the observations of the quail
z <- c(rep(0,t))
z[1] <- measurement(x[1])

# Create a matrix to hold the positions of each of the particles
x.P <- array(0, c(N,t))

# Create a matrix to hold the observations of the particles
z.P <- array(0, c(N,t))

# Initialise the particles. The prior particle distribution is modelled as
# a Gaussian around the true initial value
x.P[,1] <- rnorm(N, x[1], sqrt(V))
for (i in 1:N) {
  z.P[i,1] <- measurement(x.P[i,1])
}

# Show the distribution of particles around the initial value
par(mfrow=c(1,2))
plot(rep(1,N), x.P[,1], main="Position", pch=".", col="red", 
     xlab="time step", ylab="flight position")
hist(x.P[,1], xlab="flight position", ylab="count", main="Histogram of position")

# Create a matrix to hold the probability of each particle
P.w <- array(0, c(N,t))

# Create a vector to hold the estimated position of the quail
x.est <- c(rep(0,t))
x.est[1] <- mean(x.P[,1])

for (t in 2:t) {
  
  # From the previous time step, update the flight position and the observed
  # position (ground truth) of the quail
  x[t] = update.position(x[t-1], t)
  z[t] = measurement(x[t])
  
  # Particle filter
  for (i in 1:N) {
    # Given the prior set of particles run each of the particles through the
    # state update model to make a new set of transitioned particles
    x.P[i,t] <- update.position(x.P[i,t-1], t)
    
    # Update the observation (without any noise)
    z.P[i,t] <- x.P[i,t]^2/20

    # Generate the weights for the particles. The weights are based upon the 
    # probability of the given observation for a particle GIVEN the actual
    # observation
    P.w[i,t] <- obs.prob(z[t], z.P[i,t])
  } 
  
  # Normalise the probability distribution to sum to 1
  column.total <- sum(P.w[,t])
  P.w[,t] <- P.w[,t] / column.total
  
  # Resampling -- randomly sample from the new distribution to get new estimates
  copy <- x.P[,t]
  for (i in 1:N) {
    index <- which(rmultinom(1, 1, P.w[,t])[,1] == 1)
    x.P[i,t] <- copy[index]
  }
    
  #cum.sum.P <- cumsum(P.w[,t])
  #copy <- x.P[,t]
  #for (i in 1:N) {
  #  r <- runif(1, 0, 1)  # draw one sample from a uniform distribution on [0,1]
  #  index <- tail(which(r <= cum.sum.P), 1)
  #  stopifnot(index > 0, index <= N)  # check the index is within bounds
  #  x.P[i,t] <- copy[index]
  #}
  
  
  
  # Get the final estimate
  x.est[t] <- mean(x.P[,t])
  
}

# Plot the flight of the quail
par(mfrow=c(1,1))
plot(x, col="red")
lines(x, xlab="Time index", ylab="Position", lwd=2)
lines(x.est, col="blue")