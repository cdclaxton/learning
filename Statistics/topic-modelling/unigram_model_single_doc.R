# Unigram model - single document

library(MCMCpack)
library(rjags)

# Generate the observations
# ------------------------------------------------------------------------------

N = 5  # Number of words in the vocabulary
alpha = rep(1,N)
theta = rdirichlet(1, alpha)

lam = 5  # Mean of the Poisson distribution
N_words = rpois(1, lam)
w = rmultinom(1, N_words, theta)

# Bayesian model
# ------------------------------------------------------------------------------

# Specify the Bayesian model and save to a file
model.string <- "
model {

  theta ~ ddirch(alpha)
  w ~ dmulti(theta, N_words)

}
"
writeLines(model.string, con = "temp_model.txt")

# Data
data <- list(alpha=alpha, N_words=sum(w), w=w)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("theta"), n.iter = 1000)
plot(samples)
summary(samples)
