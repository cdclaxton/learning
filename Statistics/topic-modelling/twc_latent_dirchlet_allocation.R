# Topic-Weakly-Correlated Latent Dirichlet Allocation (TWC-LDA)

library(MCMCpack)
library(rjags)

# Generate the observations
# ------------------------------------------------------------------------------

N_topics = 2  # Number of topics
M = 6  # Number of documents in the corpus
N = 5  # Number of words in the vocabulary

lam = 100  # Mean of the Poisson distribution of the number of words in a document
N_words = rpois(M, lam)  # Number of words in the document

alpha = rep(0.5, N_topics)

# Per-topic word distribution
Beta = matrix(0, nrow=N_topics, ncol=N)
Beta[1,1:N] = c(0.80, 0.17, 0.01, 0.01, 0.01)
Beta[2,1:N] = c(0.01, 0.01, 0.30, 0.40, 0.28)

# Empty matrix for the latent topic for each word in each document
Z = matrix(0, nrow=M, ncol=max(N_words))
W = matrix(0, nrow=M, ncol=max(N_words))

# Walk over each document
Theta = matrix(0, nrow=M, ncol=N_topics)
for (doc in 1:M) {
  
  # Document-specific topic proportions
  Theta[doc, 1:N_topics] = rdirichlet(1, alpha)
  
  for (word in 1:N_words[doc]) {
    # Latent topic of the word
    Z[doc, word] =  which(rmultinom(1, 1, Theta[doc, 1:N_topics]) == 1)
    
    # Word
    W[doc, word] = which(rmultinom(1, 1, Beta[Z[doc, word], 1:N]) == 1) 
  }
}

# Bayesian model
# ------------------------------------------------------------------------------

# Specify the Bayesian model and save to a file
model.string <- "
model {
  
  # Per-topic word distribution
  for (topic in 1:N_topics) {
    Beta[topic, 1:N] ~ ddirch(alpha.beta)
  }

  # Constrain beta
  # Calcuate the sum of the inner products
  for (i in 1:(N_topics-1)) {
    for (j in (i+1):N_topics) {
      total[i,j] <- sum(Beta[i, 1:N] * Beta[j, 1:N])
    }
    totals[i] <- sum(total[i, (i+1):N_topics])
  }
  sum.inner.products <- sum(totals)  

  # Add a little bit of noise so the value can be inferred
  tau <- 500
  s ~ dnorm(sum.inner.products, tau)

  # Walk through each document
  for (doc in 1:M) {
    
    # Topic distribution for the document
    Theta[doc, 1:N_topics] ~ ddirch(alpha.theta)

    for (word in 1:N_words[doc]) {
      
      # Latent topic of the word
      Z[doc, word] ~ dcat(Theta[doc, 1:N_topics])

      # Word
      W[doc, word] ~ dcat(Beta[Z[doc, word], 1:N])
    }
  }

}
"
writeLines(model.string, con = "temp_model.txt")

# Data
alpha.theta = rep(0.1, N_topics)
alpha.beta = rep(0.1, N)   # where N = number of words in vocabulary
data <- list(M=nrow(W), 
             N=N,
             N_topics=N_topics,
             N_words=N_words,
             alpha.beta=alpha.beta, 
             alpha.theta=alpha.theta,
             W=W,
             s=0)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 10000)
update(model, n.iter = 1000)
samples <- coda.samples(model, variable.names = c("Theta", "sum.inner.products"), n.iter = 1000)
#plot(samples)
summary(samples)

# Create a matrix of sample values
m <- as.matrix(samples)

hist(m[,"sum.inner.products"])

par(mfrow=c(3,2))
hist(m[,"Theta[1,1]"])
hist(m[,"Theta[1,2]"])
hist(m[,"Theta[2,1]"])
hist(m[,"Theta[2,2]"])
hist(m[,"Theta[3,1]"])
hist(m[,"Theta[3,2]"])

print(Theta)
