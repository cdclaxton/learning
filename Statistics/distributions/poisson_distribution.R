# Poisson distribution

library(rjags)

# Generate the observations
lam = 1.2  # Mean of the Poisson distribution
N = 100   # Number of observations
obs = rpois(N, lam)

# Specify the Bayesian model and save to a file
model.string <- "
model {
  lam ~ dgamma(3, 1)   # Prior

  for (i in 1:N) {
    p[i] ~ dpois(lam)      # Likelihood
  }
}
"
writeLines(model.string, con = "temp_model.txt")

# Data
data <- list(p = obs, N=length(obs))

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("lam"), n.iter = 1000)
plot(samples)
summary(samples)