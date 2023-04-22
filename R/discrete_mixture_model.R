# Mixture model of discrete (categorical) distributions.
# 
# There are two categorical distributions (denoted x1 and x2) and they are
# selected through a Bernoulli random variable m.

library(rjags)

# JAGS model
model_string <- "
model {
    x1 ~ dcat(pi1)
    x2 ~ dcat(pi2)

    m ~ dbern(theta)  # Select model x1?

    y <- x1*m + x2*(1-m)
}
"

pi1 <- c(0.3, 0.4, 0.2, 0.1)  # Prior for x1
pi2 <- c(0.9, 0.1, 0.0, 0.0)  # Prior for x2
theta <- 0.8                  # Prior for Bernoulli RV

model <- jags.model(textConnection(model_string),
    data = list(pi1=pi1, pi2=pi2, theta=theta))

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("x1", "x2", "m", "y"),
    n.iter = 20000,
    progress.bar = "none")

#plot(samples)

# Get a matrix of the samples
mat <- as.matrix(samples)

# Count the occurrence of each value of y
y_samples <- mat[, "y"]
prob_y <- rep(0, max(y_samples))
for (i in 1:max(y_samples)) {
    prob_y[i] <- sum(y_samples == i)
}
prob_y <- prob_y / sum(prob_y)
cat("Using JAGS: ", prob_y, "\n")

# Analytically determine the probability distribution
y_analytical <- rep(0, length(pi1))
for (i in 1:length(pi1)) {
    y_analytical[i] <- pi1[i] * theta + pi2[i] * (1 - theta)
}
cat("Analytical: ", y_analytical, "\n")

# Calculate the error
sse <- sum((prob_y - y_analytical)**2)
cat("Sum of squares error: ", sse, "\n")