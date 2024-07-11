# Uncorrelated Dirichlet samples

library(MCMCpack)
library(rjags)

# Specify the Bayesian model and save to a file
model.string <- "
model {

  for (i in 1:K) {
    beta[i, 1:N] ~ ddirch(alpha)
  }

  # Sum of the inner products
  for (i in 1:(K-1)) {
    for (j in (i+1):K) {
      total[i,j] <- sum(beta[i, 1:N] * beta[j, 1:N])
    }
    totals[i] <- sum(total[i, (i+1):K])
  }
  sum.inner.products <- sum(totals)

  # Add a little bit of noise so the value can be inferred
  tau <- 500
  s ~ dnorm(sum.inner.products, tau)
}
"
writeLines(model.string, con = "temp_model.txt")

# Data
alpha = c(0.5, 0.5)
K = 3
data = list(N=length(alpha), alpha=alpha, K=K, s=0)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 6000)
update(model, n.iter = 5000)
samples <- coda.samples(model, variable.names = c("sum.inner.products"), n.iter = 5000)
plot(samples)
print(summary(samples))