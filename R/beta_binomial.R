# Beta-binomial model

library(rjags)

n <- 20
Y <- 4
a <- 3
b <- 1

# JAGS model
model_string <- "
model{
    # Likelihood
    Y ~ dbinom(theta, n)

    # Prior
    theta ~ dbeta(a, b)
}
"

model <- jags.model(textConnection(model_string),
    data = list(Y = Y, n = n, a = a, b = b))

update(model, n.iter = 10000, progress.bar = "none")

samp <- coda.samples(model,
    variable.names = c("theta"),
    n.iter = 20000,
    progress.bar = "none")

summary(samp)

plot(samp)

# Maximum likelihood value of theta
m <- as.matrix(samp)
mean_theta <- mean(m[, "theta"])
print(paste("Mean of theta:", mean_theta), quote = FALSE)
