# Unigram model - multiple documents

library(MCMCpack)
library(rjags)

# Generate the observations
# ------------------------------------------------------------------------------

N = 5  # Number of words in the vocabulary
alpha = rep(1,N)
theta = rdirichlet(1, alpha)

N_docs = 4  # Number of documents in the corpus

lam = 5  # Mean of the Poisson distribution of the number of words in a document
N_words = rpois(N_docs, lam)  # Number of words in each document

# Create an matrix of word counts in each document
W = matrix(0, nrow=N_docs, ncol=N)
for (doc in 1:N_docs) {
  W[doc,1:N] = t(rmultinom(1, N_words[doc], theta))
}

# Check the word counts are correct
stopifnot(all(N_words == rowSums(W)))

# Bayesian model
# ------------------------------------------------------------------------------

# Specify the Bayesian model and save to a file
model.string <- "
model {

  theta ~ ddirch(alpha)

  for (doc in 1:M) {
    W[doc,1:N] ~ dmulti(theta, N_words[doc])
  }

}
"
writeLines(model.string, con = "temp_model.txt")

# Data
data <- list(alpha=alpha, N_words=rowSums(W), W=W, M=nrow(W), N=ncol(W))

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("theta"), n.iter = 1000)
plot(samples)
summary(samples)
