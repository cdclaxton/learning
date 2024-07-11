# Memoryless changepoint model
# ==============================================================================

library(rjags)

# ------------------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------------------

num.time.steps <- 100
p.change <- 0.01
lambda <- c(1.0, 10.0)
initial.state <- 0

# ------------------------------------------------------------------------------
# Generate the data
# ------------------------------------------------------------------------------

# Create the vector of changepoints (note the first sample can't correspond to
# a changepoint)
changepoints <- rbinom(num.time.steps, 1, p.change)
changepoints[1] <- 0

# Build a vector of the states
states <- rep(NA, num.time.steps)
states[1] <- initial.state
for (i in 2:num.time.steps) {
  states[i] <- if (!changepoints[i]) states[i-1] else (1 - states[i-1])
}

# Generate data for the two states (ignoring changepoints at the moment)
data1 <- rpois(num.time.steps, lambda[1])
data2 <- rpois(num.time.steps, lambda[2])

# Generate the data taking into account the changepoints
d <- ((1-states) * data1) + (states * data2)

# Create a plot of the data and the changepoints
plot(d, xlab = "Time index", ylab = "Value", pch=18, col="blue")
abline(v=which(changepoints == 1), col="gray60")

# ------------------------------------------------------------------------------
# Perform inference
# ------------------------------------------------------------------------------

# Specify the model and save to a file
model.string <- "
model {

  # Probability that a change occurs at a given timestep
  theta ~ dbeta(alpha, beta)

  # Means of the Poisson distributions
  mu[1] ~ dgamma(1,0.5)
  mu[2] ~ dgamma(1,0.5)
  
  # Initialisation
  c[1] <- 0
  s[1] <- 1
  d[1] ~ dpois(mu[s[1]])

  # Walk through each timestep
  for (i in 2:num.time.steps) {

    # Is there a changepoint at timestep i?
    c[i] ~ dbern(theta)

    # If there is a changepoint, flip the state
    s[i] <- ifelse( (s[i-1] == 1) && (c[i] == 0), 1,
      ifelse( (s[i-1] == 1) && (c[i] == 1), 2,
      ifelse( (s[i-1] == 2) && (c[i] == 0), 2,
      ifelse( (s[i-1] == 2) && (c[i] == 1), 1,
      100))))  # Error state!

    # Generate the sample for the timestep
    d[i] ~ dpois(mu[s[i]])
  }
}
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list(theta = 0)

# Data
data <- list(alpha = 2, beta = 5,
             num.time.steps = num.time.steps,
             d = d)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    inits = inits, n.chains = 1, n.adapt = 5000)

update(model, n.iter = 1000)
samples <- coda.samples(model, variable.names = c("c", "s", "mu", "theta"), n.iter = 1000)

m <- as.matrix(samples)

# Find the probability that there is a changepoint at each time step
prob.changepoint <- rep(NA, num.time.steps)
for (i in 1:num.time.steps) {
  column.name <- paste0("c[", i, "]")
  prob.changepoint[i] <- mean(m[, column.name])
}

# Plot
par(mar=c(5,4,4,5)+.1)
plot(d, xlab = "Time index", ylab = "Value", pch=18, col="blue")
abline(v=which(changepoints == 1), col="red")
par(new=TRUE)
plot(prob.changepoint, type="b", col="green", xaxt="n",yaxt="n",xlab="",ylab="", ylim = c(0,1))
axis(4)
mtext("Prob. of changepoint",side=4,line=3)

mean(m[,"mu[1]"])
mean(m[,"mu[2]"])
