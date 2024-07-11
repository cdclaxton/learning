# Simple changepoint model
#
# * Changepoint is definitely present
# * Poisson distributed samples
# ==============================================================================

library(rjags)

# ------------------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------------------

num.timesteps <- 100
lambda <- c(1, 3)

# ------------------------------------------------------------------------------
# Generate the data
# ------------------------------------------------------------------------------

# Time index of the changepoint
changepoint <- round(runif(1, min=1, max=num.timesteps))

# Generate data
d <- rep(NA, num.timesteps)
for (i in 1:num.timesteps) {
  d[i] <- if (i < changepoint) rpois(1, lambda[1]) else rpois(1, lambda[2])
}

# Create a plot of the data and the changepoints
plot(d, xlab = "Time index", ylab = "Value", pch=18, col="blue")
abline(v=changepoint, col="gray60")

# ------------------------------------------------------------------------------
# Perform inference
# ------------------------------------------------------------------------------

# Specify the model and save to a file
model.string <- "
model {

  # Time of the changepoint
  c ~ dunif(1, num.timesteps)

  # Means of the Poisson distributions
  lambda[1] ~ dgamma(1,0.5)
  lambda[2] ~ dgamma(1,0.5)

  # Walk through each timestep
  for (i in 1:num.timesteps) {
    s[i] <- ifelse( (i < c), 1, 2)
    d[i] ~ dpois(lambda[s[i]])
  }
}
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list(theta = 0)

# Data
data <- list(num.timesteps = num.timesteps,
             d = d)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 5000)

update(model, n.iter = 1000)
samples <- coda.samples(model, variable.names = c("c", "lambda", "s"), n.iter = 1000)
plot(samples)

m <- as.matrix(samples)

# Find the probability that there is a changepoint at each time step
r <- round(m[,"c"])
lambda1.pred <- mean(m[,"lambda[1]"])
lambda2.pred <- mean(m[,"lambda[2]"])

prob.changepoint <- rep(NA, num.timesteps)
prob.s1 <- rep(NA, num.timesteps) 
x <- rep(NA, num.timesteps) 

for (i in 1:num.timesteps) {
  
  # Probability that a changepoint occurred at time index i
  prob.changepoint[i] <- length(which(r == i)) / length(r)
  
  # Get the probability state == 1 at timestep i
  state.name <- paste0("s[", i, "]")
  prob.s1[i] <- length(which(m[,state.name] == 1)) / length(r)
  
  # Calculate the estimated value of the samples
  x[i] <- (lambda1.pred * prob.s1[i]) + (lambda2.pred * (1 - prob.s1[i]))
}

# Plot
par(mar=c(5,4,4,5)+.1)
plot(d, xlab = "Time index", ylab = "Value", pch=18, col="blue")
lines(x, col="purple", lty=2)
abline(v=changepoint, col="red")
par(new=TRUE)
plot(prob.changepoint, type="l", col="black", xaxt="n",yaxt="n",xlab="",ylab="", ylim=c(0,1))
axis(4)
mtext("Prob. of changepoint",side=4,line=3)

