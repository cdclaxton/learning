# Bernoulli ones trick

library(rjags)

# ------------------------------------------------------------------------------
# Example: Define a normal distribution as a likelihood function
# ------------------------------------------------------------------------------

# Generate the normally distributed data
mu <- 2
sigma <- 0.1
N <- 20
y = rnorm(N, mu, sigma)

# Define the JAGS model using the 'ones trick' to define the normal PDF
modelString = "
data {
    C <- 10000
    for (i in 1:N) {
        ones[i] <- 1
    }
}
model {
    # Likelihood
    for (i in 1:N) {
        # Scaled probability of y
        spy[i] <- exp(-0.5*((y[i]-mu)/sigma)^2) / (C * sigma * (2*3.1415926)^0.5)
        ones[i] ~ dbern(spy[i])
    }
    
    # Priors
    mu ~ dunif(-5, 5)
    sigma ~ dunif(0, 2)
}
"

model <- jags.model(textConnection(modelString),
    data = list(y=y, N=N), n.chains=3, n.adapt=500)
update(model, n.iter=500)
samples = coda.samples(model, variable.names=c('mu', 'sigma'), n.iter=5000)
plot(samples)

# ------------------------------------------------------------------------------
# Example: Sum of normally distributed random variables
# ------------------------------------------------------------------------------

mu0 <- 0.5
scaling <- 1.5
mu1 <- mu0 * scaling
sigma <- 0.2
N <- 20

g0 <- rnorm(N, mu0, sigma)
g1 <- rnorm(N, mu1, sigma)

cat("mu0 = ", mean(g0), ", scaling = ", mean(g1)/mean(g0), ", sigma = ", sd(c(g0,g1)))

y <- g0 + g1

modelString = "
data {
    C <- 10000
    for (i in 1:N) {
        ones[i] <- 1
    }
}
model {
    # Likelihood
    for (i in 1:N) {
        # Scaled probability of y
        spy[i] <- exp(-0.5*((y[i]-mu)/sigma)^2) / (C * sigma * (2*3.1415926)^0.5)
        ones[i] ~ dbern(spy[i])
    }
    
    # Priors
    mu0 ~ dunif(0, 1)
    scaling ~ dunif(1, 2)
    mu1 <- mu0 * scaling
    sigma ~ dunif(0.1, 1)

    mu <- mu0 + mu1
}
"

model <- jags.model(textConnection(modelString),
    data = list(y=y, N=N), n.chains=3, n.adapt=500)
update(model, n.iter=500)
samples = coda.samples(model, variable.names=c('mu0', 'scaling', 'sigma'), n.iter=5000)
plot(samples)
