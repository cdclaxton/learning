# Uncorrelated Dirichlet samples

library(MCMCpack)
library(rjags)

# Specify the Bayesian model and save to a file
model.string <- "
model {

  beta[1, 1:N] ~ ddirch(alpha)
  beta[2, 1:N] ~ ddirch(alpha)

  sum.inner.products <- sum(beta[1, 1:N] * beta[2, 1:N])
  tau <- 500
  s ~ dnorm(sum.inner.products, tau)

  x ~ dnorm(20.0, 500)
}
"
writeLines(model.string, con = "temp_model.txt")

# Data
alpha = c(0.5, 0.5)
data = list(N=length(alpha), alpha=alpha, s=0)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 6000)
update(model, n.iter = 5000)
samples <- coda.samples(model, variable.names = c("sum.inner.products"), n.iter = 5000)
plot(samples)
print(summary(samples))