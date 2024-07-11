# Mixture of unigrams - single document

library(MCMCpack)
library(rjags)

# Generate the observations
# ------------------------------------------------------------------------------

N_topics = 2  # Number of topics
Pi = rep(1, N_topics)/N_topics  # Probability of each topic being selected
topic = which(rmultinom(1, 1, Pi) == 1)  # Topic the document is written about

N = 5  # Number of words in the vocabulary
Theta = matrix(0, nrow=N_topics, ncol=N)
for (topic in 1:N_topics) {
  alpha = rep(1,N)  # Same alpha for all topics
  Theta[topic,1:N] =  rdirichlet(1, alpha)
}

lam = 100  # Mean of the Poisson distribution of the number of words in a document
N_words = rpois(1, lam)  # Number of words in the document

w = rmultinom(1, N_words, Theta[topic,1:N])

# Bayesian model
# ------------------------------------------------------------------------------

# Specify the Bayesian model and save to a file
model.string <- "
model {

  # Topic the document was written about
  topic ~ dcat(Pi)

  # Build the theta distribution for each topic
  for (i in 1:N_topics) {
    theta[i, 1:N] ~ ddirch(alpha)
  }

  # Select the word counts
  w ~ dmulti(theta[topic,1:N], N_words)
}
"
writeLines(model.string, con = "temp_model.txt")

# Data
data <- list(Pi=Pi, N_topics=length(Pi), alpha=alpha, N=length(w), w=w, N_words=sum(w))

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("topic", "theta"), n.iter = 1000)
plot(samples)
summary(samples)

m <- as.matrix(samples)
head(m)

# Calculate the Theta matrix from inferred values
Theta_mu = matrix(0, nrow=N_topics, ncol=N)
for (topic in 1:N_topics) {
  for (word in 1:N) {
    name = paste0("theta[", topic, ",", word, "]")
    Theta_mu[topic, word] = mean(m[,name])
  }
}

print(paste0("Topic: ", mean(m[,"topic"])))
print(Theta)
print(Theta_mu)
