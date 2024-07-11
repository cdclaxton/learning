# Mixture of unigrams -- multiple documents

library(MCMCpack)
library(rjags)

# Generate the observations
# ------------------------------------------------------------------------------

N_topics = 2  # Number of topics
Pi = rep(1, N_topics)/N_topics  # Probability of each topic being selected

M = 6  # Number of documents in the corpus
N = 5  # Number of words in the vocabulary

lam = 100  # Mean of the Poisson distribution of the number of words in a document
N_words = rpois(M, lam)  # Number of words in the document

# Matrix of probability of each word being selected for each topic
#Theta = matrix(0, nrow=N_topics, ncol=N)
#for (topic in 1:N_topics) {
#  alpha = rep(1,N)  # Same alpha for all topics
#  Theta[topic, 1:N] = rdirichlet(1, alpha)
#}

alpha = rep(1,N)  # Same alpha for all topics

Theta = matrix(0, nrow=N_topics, ncol=N)
Theta[1,1:N] = c(0.4, 0.4, 0.2, 0.0, 0.0)
Theta[2,1:N] = c(0.0, 0.0, 0.2, 0.4, 0.4)

# Empty matrix of word counts in each document
W = matrix(0, nrow=M, ncol=N)

# Walk through each document
topic = rep(NA, M)
for (doc in 1:M) {
  # Topic from which the document was generated
  topic[doc] = which(rmultinom(1, 1, Pi) == 1)
  
  # Word counts
  W[doc, 1:N] = rmultinom(1, N_words[doc], Theta[topic[doc],1:N])
}

# Bayesian model
# ------------------------------------------------------------------------------

# Specify the Bayesian model and save to a file
model.string <- "
model {

  # Build the theta distribution for each topic
  for (i in 1:N_topics) {
    theta[i, 1:N] ~ ddirch(alpha)
  }

  # Walk through each document
  for (doc in 1:M) {
  
    # Select the topic the document was written about
    topic[doc] ~ dcat(Pi)

    # Select the word counts in the document
    W[doc,1:N] ~ dmulti(theta[topic[doc],1:N], N_words[doc])
  }
}
"
writeLines(model.string, con = "temp_model.txt")

# Data
data <- list(M=nrow(W), Pi=Pi, N_topics=length(Pi), alpha=alpha, N_words=rowSums(W), N=ncol(W),
             W=W)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 1000)
update(model, n.iter = 1000)
samples <- coda.samples(model, variable.names = c("topic", "theta"), n.iter = 1000)
#plot(samples)
summary(samples)

# Create a matrix of sample values
m <- as.matrix(samples)

# Build the inferred theta matrix
Theta_mu = matrix(0, nrow=N_topics, ncol=N)
for (t in 1:N_topics) {
  for (word in 1:N) {
    name = paste0("theta[", t, ",", word, "]")
    Theta_mu[t, word] = mean(m[,name])
  }
}

# Plot the probabilities that each document is due to the topic
par(mfrow=c(3,3))
max.plot = if (M <= 9) M else 9
for (doc in 1:max.plot) {
  name = paste0("topic[", doc, "]")
  hist(m[,name], col='red', xlim=c(-1,3), xlab='topic', main = paste0("Doc ", doc))
}
