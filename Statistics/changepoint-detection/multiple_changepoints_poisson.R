# Changepoint model with zero, one or two changepoints
#
# * Changepoints are potentially present
# * Poisson distributed samples
# ==============================================================================

library(rjags)

# ------------------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------------------

num.time.steps <- 100
lambda <- c(1, 3, 8)
p.changepoints <- c(0.2, 0.4, 0.4)

# ------------------------------------------------------------------------------
# Generate the data
# ------------------------------------------------------------------------------

# Number of change-points in the data
n.changepoints <- which(rmultinom(1, 1, p.changepoints) == 1) - 1

# Get the time indices of the change-points
if (n.changepoints == 0) {
  changepoints <- NA
} else if (n.changepoints == 1) {
  changepoints <- round(runif(1, 1, num.time.steps))
} else {
  changepoints <- sort(c(
    round(runif(1, min = 1, max = num.timesteps)),
    round(runif(1, min = 1, max = num.timesteps))
  ))
}

# Generate the data for each of the time steps (this could be optimised)
d <- rep(NA, num.time.steps)
for (i in 1:num.time.steps) {
  if (n.changepoints == 0) {
    changepoints <- NA
    d[i] <- rpois(1, lambda[1])
  } else if (n.changepoints == 1) {
    d[i] <- if (i < changepoints) rpois(1, lambda[1]) else rpois(1, lambda[2])
  } else {
    if (i < changepoints[1]) {
      d[i] <- rpois(1, lambda[1])
    } else if (i < changepoints[2]) {
      d[i] <- rpois(1, lambda[2])
    } else {
      d[i] <- rpois(1, lambda[3])
    }
  }
}

# Plot the data
plot(d, xlab = "Time index", ylab = "Value", pch = 18, col = "blue")
if (n.changepoints > 0) abline(v = changepoints, col = "gray60")

# ------------------------------------------------------------------------------
# Perform inference
# ------------------------------------------------------------------------------

# Specify the model and save to a file
model.string <- "
model {

  # Number of regions
  theta ~ ddirch(alpha)
  n ~ dcat(theta)

  # Means of the Poisson distributions
  for (i in 1:3) {
    lambda[i] ~ dgamma(1,0.5)
  }

  # Signs of the deltas
  delta[1] ~ dbern(0.5)
  delta[2] ~ dbern(0.5)

  s[1] <- ifelse(delta[1] == 1, 1, -1)
  s[2] <- ifelse(delta[2] == 1, 1, -1)

  # Potential change-points
  j ~ dunif(2, N)
  k ~ dunif(j+1, N)

  lambda.region1 <- lambda[1]
  lambda.region2a <- lambda[1] + (s[1] * lambda[2])
  lambda.region3a <- lambda[1] + (s[1] * lambda[2]) + (s[2] * lambda[3])

  lambda.region2 <- ifelse(lambda.region2a < 0, 0, lambda.region2a)
  lambda.region3 <- ifelse(lambda.region3a < 0, 0, lambda.region3a)

  # Generate the data
  for (i in 1:N) {

    l[i] <- lambda[1] +
      ((i > j && n > 1) * s[1] * lambda[2]) +
      ((i > k && n > 2) * s[2] * lambda[3])

    d[i] ~ dpois(l[i])
  }
}
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list()

# Data
data <- list(
  alpha = c(0.8, 0.2, 0.1),
  d = d,
  N = length(d)
)

# Build the JAGS model
model <- jags.model(
  file = "temp_model.txt", data = data,
  n.chains = 1, n.adapt = 500
)
update(model, n.iter = 500)
samples <- coda.samples(model,
  variable.names = c(
    "n", "lambda", "j", "k",
    "lambda.region1", "lambda.region2", "lambda.region3"
  ),
  n.iter = 1000
)
# plot(samples)

m <- as.matrix(samples)
head(m)

# Find the most likely number of regions
getmode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}

n.mle <- getmode(m[, "n"])
cat("MLE of the number of regions = ", n.mle)

# ------------------------------------------------------------------------------
# Plot
# ------------------------------------------------------------------------------

# Find the probability that there is a changepoint at each time step
c1.rounded <- round(m[, "j"])
c2.rounded <- round(m[, "k"])
n <- m[, "n"]

prob.changepoint1 <- rep(NA, num.time.steps)
prob.changepoint2 <- rep(NA, num.time.steps)

prob.changepoint1.mle <- rep(NA, num.time.steps)
prob.changepoint2.mle <- rep(NA, num.time.steps)

for (i in 1:num.time.steps) {
  # Probability that a changepoint occurred at time index i
  prob.changepoint1[i] <- length(which(c1.rounded == i)) / length(n)
  prob.changepoint2[i] <- length(which(c2.rounded == i)) / length(n)

  # Probability that a changepoint occurred at time index i given the MLE
  # of n
  l.mle <- length(which(n == n.mle))
  prob.changepoint1.mle[i] <- length(which(c1.rounded == i & n == n.mle)) / l.mle
  prob.changepoint2.mle[i] <- length(which(c2.rounded == i & n == n.mle)) / l.mle
}

# Plot
par(mar = c(5, 4, 4, 5) + .1)
plot(d, xlab = "Time index", ylab = "Value", pch = 18, col = "blue")
# lines(x, col="purple", lty=2)
abline(v = changepoints, col = "gray60")
par(new = TRUE)
plot(prob.changepoint1,
  type = "l", lty = 2, col = "green",
  xaxt = "n", yaxt = "n", xlab = "", ylab = "", ylim = c(0, 1)
)
lines(prob.changepoint1.mle, type = "l", lty = 1, col = "green")
lines(prob.changepoint2, type = "l", lty = 2, col = "red")
lines(prob.changepoint2.mle, type = "l", lty = 1, col = "red")
axis(4)
mtext("Prob. of changepoint", side = 4, line = 3)
