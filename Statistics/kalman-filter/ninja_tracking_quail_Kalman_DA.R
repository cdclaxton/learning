# Ninja tracking quail
# with Data Association
# (http://studentdavestutorials.weebly.com/kalman-filter-with-matlab-code.html)

library(MASS)

# Define the meta-variables
duration <- 10  # how long the quail flies for
dt <- 0.1  # how often the ninja gets samples

# Define the update equations (cofficient matrices)
A <- matrix(c(1, 0, dt, 1), nrow = 2)  # state transition matrix
B <- matrix(c(dt^2/2, dt), nrow = 2)  # input control matrix
C <- matrix(c(1, 0), nrow = 1)  # measurement matrix

# Define the number of spurious observations and their spread
lambda <- 5
pos.min <- 0
pos.max <- 80

# Define the main variables
times <- seq(0, duration, dt)
u <- 1.5  # acceleration magnitude
Q <- matrix(c(0,0), nrow = 2)  # initialised state (position, velocity)
Q.est <- Q  # estimate of the state
quail.accel.noise.mag <- 1.05  # process noise (std. dev. of acceleration)
ninja.vision.noise.mag <- 10  # measurement noise (std. dev. of location)
Ez <- ninja.vision.noise.mag^2  # convert measurement noise to covariance matrix
Ex <- quail.accel.noise.mag^2 * matrix(c(dt^4/4, dt^3/2, dt^3/2, dt^2), nrow = 2)
P <- Ex

# Initialise result variables
Q.loc <- c()  # actual quail flight path
vel <- c()  # actual quail velocity
Q.loc.meas <- vector("list", length(times))  # quail path that the ninja sees

# Simulate what the ninja sees over time
for (ti in 1:length(times)) {
 
  # Generate the quail flight
  quail.accel.noise <- quail.accel.noise.mag * 
    matrix(c(dt^2/2 * rnorm(1,0,1), dt * rnorm(1,0,1)))
  Q <- A %*% Q + B %*% u + quail.accel.noise
  
  # Generate an observation due to the quail's position
  ninja.vision.noise <- ninja.vision.noise.mag * rnorm(1,0,1)
  y <- C %*% Q + ninja.vision.noise
  
  # Generate spurious observations
  n <- rpois(1, lambda)
  pts <- runif(n, pos.min, pos.max)
  pts <- c(y, pts)
  
  # Store the actual location and velocity of the quail
  Q.loc <- c(Q.loc, Q[1])
  vel <- c(vel, Q[2])
  
  # Store the observations (positions)
  Q.loc.meas[[ti]] <- pts
}

# Plot the path of the quail
plot(times, Q.loc, col = "red", xlab = "time", ylab = "position",
     ylim = c(-20, 100))
for (ti in 1:length(times)) {
  # Plot the observation due to the quail
  points(times[ti], Q.loc.meas[[ti]][1], col = "black", pch = 20)
  
  # Plot the spurious observations (if there are any)
  spurious.pts <- Q.loc.meas[[ti]][-1]
  t <- rep(times[ti], length(spurious.pts))
  points(t, spurious.pts, col = "blue", pch = '*')
}

# Data association functions
gate <- function(predicted, observations, max.dist) {
  # Gating function.
  diff <- abs(observations - predicted)
  indices <- which(diff < max.dist)
  matches <- observations[indices]
  
  # Ensure that at least one observation is returned
  if (length(matches) == 0) {
    observations[which.min(diff)]
  } else {
    matches
  }
}

gnn <- function(predicted, observations) {
  # Global Nearest Neighbour (GNN).
  diff <- abs(observations - predicted)
  index <- which.min(diff)
  observations[index]
} 

# Perform Kalman filtering
Q.loc.est <- c()  # quail position estimate
vel.est <- c()  # quail velocity estimate
Q <- matrix(c(0,0), nrow = 2)
P.est <- P
P.mag.est <- c()
predicted.state <- c()
predicted.variance <- c()

da.method <- "gnn"
max.gate.dist <- 50
zt.gnn <- c()

for (ti in 1:length(times)) {
  
  # Predict the next state of the quail using the last state and the predicted motion
  Q.est <- A %*% Q.est + B %*% u
  predicted.state <- c(predicted.state, Q.est[1])
  
  # Predict the next covariance
  P <- A %*% P %*% t(A) + Ex
  predicted.variance <- c(predicted.variance, P)
  
  # Kalman gain
  K <- (P %*% t(C)) %*% ginv(C %*% P %*% t(C) + Ez)
  
  # Perform data association
  if (da.method == "gnn") {
    gated.obs <- gate(Q.est[1], Q.loc.meas[[ti]], max.gate.dist)
    zt <- gnn(Q.est[1], gated.obs)
    zt.gnn <- c(zt.gnn, zt)
  }
  
  # Update the state estimate
  Q.est <- Q.est + K %*% (zt - C %*% Q.est)
  
  # Update the covariance estimate
  P = (diag(2) - K %*% C) %*% P
  
  # Store for plotting
  Q.loc.est <- c(Q.loc.est, Q.est[1])
  vel.est <- c(vel.est, Q.est[2])
  P.mag.est <- c(P.mag.est, P[1])
}

# Plot the path of the quail
plot(times, Q.loc, col = "red", xlab = "time", ylab = "position",
     ylim = c(-20, 100))
for (ti in 1:length(times)) {
  # Plot the observation due to the quail
  points(times[ti], Q.loc.meas[[ti]][1], col = "black", pch = 20)
  
  # Plot the spurious observations (if there are any)
  spurious.pts <- Q.loc.meas[[ti]][-1]
  t <- rep(times[ti], length(spurious.pts))
  points(t, spurious.pts, col = "blue", pch = '*')
}
lines(times, Q.loc.est, type = 'l', col = "green")

# Add data association-specific plots
if (da.method == "gnn") {
  lines(times, zt.gnn, col = "purple")
}
