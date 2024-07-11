# Time-dependent Poisson distribution with a potential outlier.
#
# Without an outlier, the mean of the Poisson distribution is given by:
# \lambda(t) =  max(\alpha * t + \beta, 0)
#
# With a potential outlier:
# \lambda(t) = max(\alpha * t + \beta + \eta \delta(t_0), 0)
# where
#   \eta is a selection variable, \eta \in {0,1}
#   \delta_(t_0) is the time of the outlier
#
# ==============================================================================

library(ks)
library(rjags)

# ------------------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------------------

num.time.steps <- 100
alpha.true <- runif(1, -0.25, 0.25)
beta.true <- rnorm(1, 5, 2)
p.outlier <- 0.99
lambda.outlier <- 20

# ------------------------------------------------------------------------------
# Generate the data
# ------------------------------------------------------------------------------

time <- 0:(num.time.steps-1)
lambda.true <- pmax(alpha.true * time + beta.true, 0)

# Generate the samples
x <- rep(NA, num.time.steps)
for (i in 1:num.time.steps) {
  x[i] <- rpois(1, lambda.true[i])
}

# If there is an outlier, add it to the data
outlier.present <- rbinom(1, 1, p.outlier)
outlier.time <- round(runif(1, min=1, max=num.time.steps))
outlier.value <- rpois(1, lambda.outlier)

if (outlier.present) {
  x[outlier.time] <- x[outlier.time] + outlier.value
}

# Plot the data
plot(x, xlab = "Time index", ylab = "Value", pch=20)
lines(lambda.true, col = "red")
if (outlier.present) {
  points(x = outlier.time, y = x[outlier.time], col="green", pch=19)
}

# ------------------------------------------------------------------------------
# Perform inference
# ------------------------------------------------------------------------------

# Specify the model and save to a file
model.string <- "
model {
  # Convert std. dev. to precision
  alpha.tau <- 1/(alpha.sd * alpha.sd)
  beta.tau <- 1/(beta.sd * beta.sd)

  alpha ~ dnorm(alpha.mu, alpha.tau)
  beta ~ dnorm(beta.mu, beta.tau)

  # Outlier present?
  #p.outlier ~ dunif(0, 0.01)
  #p.outlier ~ dbeta(p.outlier.alpha, p.outlier.beta)
  #outlier.present ~ dbern(p.outlier)

  outlier.present ~ dbern(0.5)

  outlier.value.mean ~ dgamma(lambda.outlier.shape, lambda.outlier.rate)
  outlier.value ~ dpois(outlier.value.mean)
  outlier.time ~ dunif(1, N)

  for (i in 1:N) {
    lambda.clean[i] <- max((alpha * i) + beta, 0.00001)
    lambda[i] <- ifelse(i == round(outlier.time), 
                        lambda.clean[i]+outlier.value, 
                        lambda.clean[i])

    x[i] ~ dpois(lambda[i])
  }

}
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list()

# Data
data <- list(x = x, N = length(x),
             alpha.mu = 0, alpha.sd = 5,
             beta.mu = 0, beta.sd = 5,
             lambda.outlier.shape = 1, lambda.outlier.rate = 0.5)
             #p.outlier.alpha = 2, p.outlier.beta = 2)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 1000)
update(model, n.iter = 100)
samples <- coda.samples(model, 
                        variable.names = c("alpha", "beta",
                                           "outlier.present", "outlier.time",
                                           "outlier.value"),
                        n.iter = 1000)
#plot(samples)
summary(samples)

m <- as.matrix(samples)
head(m)

# Get the mode of a vector
getmode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}

# Plot the mean superimposed on the points
alpha.est <- m[,"alpha"]
beta.est <- m[,"beta"]
outlier.present.est <- m[,"outlier.present"]
outlier.time.est <- round(m[,"outlier.time"])
outlier.value.est <- m[,"outlier.value"]

# Generate the title
est.prob.outlier <- mean(outlier.present.est)
est.time <- getmode(outlier.time.est)

if (outlier.present) {
  titles <- list(
    bquote(t[actual] == .(outlier.time)),
    bquote(t[MLE] == .(est.time)),
    bquote(P[outlier] == .(est.prob.outlier)))
    
} else {
  titles <- list(
    "No actual outlier present",
    bquote(t[MLE] == .(est.time)),
    bquote(P[outlier] == .(est.prob.outlier)))
}

plot(x, xlab = "Time index", ylab = "Value", pch=20, col = rgb(0, 0, 0, 0.3))
invisible(mapply(mtext, text = titles, line = seq_along(titles)))

for (i in 1:nrow(m)) {
  lambda.est <- pmax(alpha.est[i] * time + beta.est[i], 0)
  
  if (outlier.present.est[i] > 0) {
    j <- outlier.time.est[i] # Estimated time of the outlier
    lambda.est[j] <- lambda.est[j] + outlier.value.est[i]
  }
      
  lines(lambda.est, col = rgb(0, 0, 1, 0.05))
}
lines(lambda.true, col = "red")

# Overlay the outlier (if present) in green
if (outlier.present) {
  points(x = outlier.time, y = x[outlier.time], col="green", pch=19)
}

#hist(m[,"outlier.present"])
#hist(m[,"outlier.time"])

#outlier.time.kde <- kde(x = m[,"outlier.time"], positive = TRUE)
#plot(outlier.time.kde, col=3, xlab="Time index")

#kde.p.outlier <- kde(x = m[,"p.outlier"], positive = TRUE)
#plot(kde.p.outlier, col = "green")
