# Sine wave model with outliers
#
# Model:
# - Number of communications between entities in a clique.
# - Very simple day/night pattern
# - Event may occur where the pattern is disrupted for a period of time
#
# ==============================================================================

library(rjags)

# ------------------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------------------

num.time.steps <- 48

omega <- pi/12
a <- 6
b <- 6
phi <- 3*(2*pi / 24)

p.event <- 0.9
lambda.event <- 0.1
max.event.duraton <- 8

# ------------------------------------------------------------------------------
# Generate the data
# ------------------------------------------------------------------------------

call.gen <- function(a, b, omega, time, phi) {
  # Generate the mean number of calls
  #
  # Args:
  #   a: Amplitude.
  #   b: Offset.
  #   omega:
  #   time: Vector of times at which to calculate the number of calls.
  #   phi: Phase.
  # 
  # Returns:
  #   Vector of mean number of calls.
  
  b + (a * sin(omega * time + phi))
}

call.gen.with.event <- function(a, b, omega, time, phi, 
                                event, ts, te, lambda.event) {
  # Generate the mean number of calls
  #
  # Args:
  #   a: Amplitude.
  #   b: Offset.
  #   omega:
  #   time: Vector of times at which to calculate the number of calls.
  #   phi: Phase.
  #   event: Event occurred?
  #   ts: Start time.
  #   te: End time.
  #   lambda.event: Mean during the event.
  # 
  # Returns:
  #   Vector of mean number of calls.
  
  # Preconditions
  stopifnot(ts <= te)
  
  # Generate the number of calls without an event
  lambda <- call.gen(a, b, omega, time, phi)
  
  # If there is an event, modify the mean
  if (event) {
    lambda[te:ts] <- lambda.event
  }
  
  return(lambda)
}


# Time (in hours)
time <- 0:(num.time.steps-1)

# Mean of the Poisson distribution
lambda.no.event <- call.gen(a, b, omega, time, phi)

# Model: Duration of the event is unknown
ts <- round(runif(1, 0, max(time)))

max.end.time <- min(ts + max.event.duraton, max(time))
te <- round(runif(1, ts, max.end.time))

# Event occurred?
event <- rbinom(1, 1, p.event)

lambda <- call.gen.with.event(a, b, omega, time, phi,
                              event, ts, te, lambda.event)

# Generate the actual samples
x <- rep(NA, length(time))
for (i in 1:length(time)) {
  x[i] <- rpois(1, lambda[i])
}

# Plot the data
plot(time, x, xlab = "Hour", ylab = "Number of calls", 
     pch=20, col = rgb(0, 0, 0, 0.3))
lines(lambda, col="red")
lines(lambda.no.event, col="red", lty=3)

# ------------------------------------------------------------------------------
# Perform inference
# ------------------------------------------------------------------------------

# Specify the model and save to a file
model.string <- "
model {

  # Amplitude
  a ~ dunif(1, 10)

  # Offset (need to ensure lambda is always >= 0)
  b.pre ~ dexp(0.5)
  b <- b.pre + a

  # Phase
  pi <- 3.1415926536
  phi.hours ~ dunif(-12, 12)
  phi <- phi.hours*(2*pi / 24)

  # Did an event occur?
  event ~ dbern(0.5)

  # Event start time
  ts.float ~ dunif(1,N-1)
  ts <- round(ts.float)
  
  # Event end time
  te.float ~ dunif(ts, N)
  te <- round(te.float)

  # Mean number of calls during the event
  lambda.event ~dunif(0,30)  #dexp(0.5)
  
  for (i in 1:N) {

    # Build lambda without an event
    lambda.without.event[i] <- (a * sin((pi/12 * i) + phi)) + b

    # Build lambda with a potential event
    lambda[i] <- ifelse( event && i >= ts && i <= te, 
                          lambda.event,
                          lambda.without.event[i])

    # Number of calls
    x[i] ~ dpois(lambda[i])
  }

}
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list()

# Data
data <- list(N = length(x),
             x = x)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 1000)
update(model, n.iter = 100)
samples <- coda.samples(model, 
                        variable.names = c("a", "b", "phi", "event", 
                                           "ts", "te", "lambda.event"),
                        n.iter = 1000)
# plot(samples)
summary(samples)

m <- as.matrix(samples)

# Get the mode of a vector
getmode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}

# Plot the data
if (event) {
  titles <- list(
    paste0("End time: Actual = ", te, ", MLE = ", getmode(m[,"te"])),
    paste0("Start time: Actual = ", ts, ", MLE = ", getmode(m[,"ts"])),
    bquote(P[event] == .(mean(m[,"event"]))))
  
} else {
  titles <- list(
    "No event present",
    bquote(P[outlier] == .(mean(m[,"event"]))))
}

plot(time, x, xlab = "Hour", ylab = "Number", 
     pch=20, col = rgb(0, 0, 0, 0.3))
invisible(mapply(mtext, text = titles, line = seq_along(titles)))

a.est <- m[,"a"]
b.est <- m[,"b"]
phi.est <- m[,"phi"]
event.est <- m[,"event"]
ts.est <- m[,"ts"]
te.est <- m[,"te"]
lambda.event <- m[,"lambda.event"]

for (i in 1:nrow(m)) {

  l.est <- call.gen.with.event(a.est[i], b.est[i], omega, time, phi.est[i],
                               event.est[i], ts.est[i], te.est[i], 
                               lambda.event[i])
  
  lines(time, l.est, col = rgb(0, 0, 1, 0.05))
}

lines(time, lambda, col="red")
lines(time, lambda.no.event, col="red", lty=3)

cat("Probability of event = ", mean(event.est))
