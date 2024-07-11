# Ninja tracking quail
# (http://studentdavestutorials.weebly.com/kalman-filter-with-matlab-code.html)

library(MASS)

# Define the meta-variables
duration <- 10  # how long the quail flies for
dt <- 0.1  # how often the ninja gets samples

# Define the update equations (cofficient matrices)
A <- matrix(c(1, 0, dt, 1), nrow = 2)  # state transition matrix
B <- matrix(c(dt^2/2, dt), nrow = 2)  # input control matrix
C <- matrix(c(1, 0), nrow = 1)  # measurement matrix

# Define the main variables
u <- 1.5  # acceleration magnitude
Q <- matrix(c(0,0), nrow = 2)  # initialised state (position, velocity)
Q.est <- Q  # estimate of the state
quail.accel.noise.mag <- 0.05  # process noise (std. dev. of acceleration)
ninja.vision.noise.mag <- 10  # measurement noise (std. dev. of location)
Ez <- ninja.vision.noise.mag^2  # convert measurement noise to covariance matrix
Ex <- quail.accel.noise.mag^2 * matrix(c(dt^4/4, dt^3/2, dt^3/2, dt^2), nrow = 2)
P <- Ex

# Initialise result variables
Q.loc <- c()  # actual quail flight path
vel <- c()  # actual quail velocity
Q.loc.meas <- c()  # quail path that the ninja sees

# Simulate what the ninja sees over time
times <- seq(0, duration, dt)
for (t in times) {
 
  # Generate the quail flight
  quail.accel.noise <- quail.accel.noise.mag * 
    matrix(c(dt^2/2 * rnorm(1,0,1), dt * rnorm(1,0,1)))
  Q <- A %*% Q + B %*% u + quail.accel.noise
  
  # Generate what the Ninja sees
  ninja.vision.noise <- ninja.vision.noise.mag * rnorm(1,0,1)
  y <- C %*% Q + ninja.vision.noise
  
  Q.loc <- c(Q.loc, Q[1])
  Q.loc.meas <- c(Q.loc.meas, y)
  vel <- c(vel, Q[2])
}

# Plot the path of the quail
plot(times, Q.loc, col = "red", xlab = "time", ylab = "position")
lines(times, Q.loc.meas, type = 'p', col = "black")

# Perform Kalman filtering
Q.loc.est <- c()  # quail position estimate
vel.est <- c()  # quail velocity estimate
Q <- matrix(c(0,0), nrow = 2)
P.est <- P
P.mag.est <- c()
predicted.state <- c()
predicted.variance <- c()

for (ti in 1:length(times)) {
  
  # Predict the next state of the quail using the last state and the predicted motion
  Q.est <- A %*% Q.est + B %*% u
  predicted.state <- c(predicted.state, Q.est[1])
  
  # Predict the next covariance
  P <- A %*% P %*% t(A) + Ex
  predicted.variance <- c(predicted.variance, P)
  
  # Kalman gain
  K <- (P %*% t(C)) %*% ginv(C %*% P %*% t(C) + Ez)
  
  # Update the state estimate
  Q.est <- Q.est + K %*% (Q.loc.meas[ti] - C %*% Q.est)
  
  # Update the covariance estimate
  P = (diag(2) - K %*% C) %*% P
  
  # Store for plotting
  Q.loc.est <- c(Q.loc.est, Q.est[1])
  vel.est <- c(vel.est, Q.est[2])
  P.mag.est <- c(P.mag.est, P[1])
}

# Plot the results
plot(times, Q.loc, col = "red", xlab = "time", ylab = "position",
     ylim = c(-20, 100))
lines(times, Q.loc.meas, type = 'o', col = "black", lwd = 0.5)
lines(times, Q.loc.est, type = 'l', col = "green")