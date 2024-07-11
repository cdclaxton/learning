# Changepoint model with two changepoints
#
# * Changepoints are definitely present
# * Poisson distributed samples
# ==============================================================================

library(rjags)

# ------------------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------------------

num.timesteps <- 100
lambda <- c(1, 3, 0.5)

# ------------------------------------------------------------------------------
# Generate the data
# ------------------------------------------------------------------------------

# Time index of the changepoints
changepoints <- sort(c(round(runif(1, min=1, max=num.timesteps)),
                       round(runif(1, min=1, max=num.timesteps))))

# Generate data
d <- rep(NA, num.timesteps)
for (i in 1:num.timesteps) {
  
  # Get the mean of the Poisson distribution for the time step
  if (i < changepoints[1]) {
    d[i] <- rpois(1, lambda[1])
  } else if (i < changepoints[2]) {
    d[i] <- rpois(1, lambda[2])
  } else {
    d[i] <- rpois(1, lambda[3])
  }
}

# Create a plot of the data and the changepoints
plot(d, xlab = "Time index", ylab = "Value", pch=18, col="blue")
abline(v=changepoints, col="gray60")

# ------------------------------------------------------------------------------
# Perform inference
# ------------------------------------------------------------------------------

# Specify the model and save to a file
model.string <- "
model {

  # Time of the changepoint
  c[1] ~ dunif(1, num.timesteps-1)
  c[2] ~ dunif(c[1], num.timesteps)
  
  # Means of the Poisson distributions
  lambda[1] ~ dgamma(1,0.5)
  lambda[2] ~ dgamma(1,0.5)
  lambda[3] ~ dgamma(1,0.5)
  
  # Walk through each timestep
  for (i in 1:num.timesteps) {
    s[i] <- ifelse( (i < c[1]), 1, ifelse( (i < c[2]), 2, 3))
    d[i] ~ dpois(lambda[s[i]])
  }
}
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list(theta = 0)

# Data
data <- list(num.timesteps = num.time.steps,
             d = d)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 5000)

update(model, n.iter = 1000)
samples <- coda.samples(model, variable.names = c("c", "lambda", "s"), n.iter = 1000)

m <- as.matrix(samples)

# Find the probability that there is a changepoint at each time step
c1.rounded <- round(m[,"c[1]"])
c2.rounded <- round(m[,"c[2]"])
lambda1.pred <- mean(m[,"lambda[1]"])
lambda2.pred <- mean(m[,"lambda[2]"])
lambda3.pred <- mean(m[,"lambda[3]"])

prob.s1 <- rep(NA, num.time.steps)
prob.s2 <- rep(NA, num.time.steps)
prob.s3 <- rep(NA, num.time.steps)

prob.changepoint1 <- rep(NA, num.time.steps)
prob.changepoint2 <- rep(NA, num.time.steps)

for (i in 1:num.time.steps) {
  
  # Probability that a changepoint occurred at time index i
  prob.changepoint1[i] <- length(which(c1.rounded == i)) / length(r)
  prob.changepoint2[i] <- length(which(c2.rounded == i)) / length(r)
  
  # Get the probability state == 1 at timestep i
  state.name <- paste0("s[", i, "]")
  prob.s1[i] <- length(which(m[,state.name] == 1)) / length(r)
  prob.s2[i] <- length(which(m[,state.name] == 2)) / length(r)
  prob.s3[i] <- length(which(m[,state.name] == 3)) / length(r)
  
  # Calculate the estimated value of the samples
  x[i] <- (lambda1.pred * prob.s1[i]) + 
    (lambda2.pred * prob.s2[i]) +
    (lambda3.pred * prob.s3[i])
}

# Plot
par(mar=c(5,4,4,5)+.1)
plot(d, xlab = "Time index", ylab = "Value", pch=18, col="blue")
lines(x, col="purple", lty=2)
abline(v=changepoints, col="red")
par(new=TRUE)
plot(prob.changepoint1, type="l", col="green", xaxt="n",yaxt="n",xlab="",ylab="", ylim=c(0,1))
lines(prob.changepoint2, type="l", col="red")
axis(4)
mtext("Prob. of changepoint",side=4,line=3)

