# Biterm topic model
# ==============================================================================

library(MCMCpack)
library(rjags)

# ------------------------------------------------------------------------------
# Generate the data
# ------------------------------------------------------------------------------

# Number of topics
k <- 2

# Hyper-parameter of the topic distribution for the whole corpus
alpha <- rep(50/k, k)

# Topic distribution for the whole corpus
theta <- rdirichlet(1, alpha)

# Number of tokens in the vocabulary
V = 8

# Hyper-parameter of the topic-specific word distribution
beta <- rep(50/V, V)

# Topic-specific word distribution (k x V)
phi <- matrix(NA, nrow=k, ncol=V)
for (i in 1:k) {
  phi[i,1:V] <- rdirichlet(1, beta)
}

# Number of biterms
len.B <- 5

# Vector to hold the topics for the biterms
z <- rep(NA, len.B)

# Vector of word indices
wi <- rep(NA, len.B)
wj <- rep(NA, len.B)

# Generate the biterms
for (i in 1:len.B) {
  
  # Generate the topic for the biterm
  z[i] <- which(rmultinom(1, 1, theta) == 1)
 
  # Given the topic, chose the biterms
  wi[i] <- which(rmultinom(1, 1, phi[z[i],1:V]) == 1)
  wj[i] <- which(rmultinom(1, 1, phi[z[i],1:V]) == 1)  
}

# ------------------------------------------------------------------------------
# Perform inference
# ------------------------------------------------------------------------------

# Specify the model and save to a file
model.string <- "
model {

  # Build hyper-parameter of the topic distribution for the whole corpus
  for (i in 1:k) {
    alpha[i] = 50/k
  }

  # Topic distribution for the whole corpus
  theta ~ ddirch(alpha[1:k])

  # Hyper-parameter of the topic-specific word distribution
  for (i in 1:V) {
    beta[i] = 50/V
  }

  # Topic-specific word distribution (k x V)
  for (i in 1:k) {
    phi[i,1:V] ~ ddirch(beta[1:V])
  } 

  # Generate the biterms
  for (i in 1:B) {
    
    # Generate the topic for the biterm
    z[i] ~ dcat(theta)

    # Given the topic, chose the biterms
    wi[i] ~ dcat(phi[z[i], 1:V])
    wj[i] ~ dcat(phi[z[i], 1:V])
  }

}
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list()

# Data
data <- list(k = k, 
             V = V,
             B = len.B,
             wi = wi,
             wj = wj)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 1000)
update(model, n.iter = 100)
samples <- coda.samples(model, 
                        variable.names = c("theta", "phi", "z"),
                        n.iter = 1000)
#plot(samples)
summary(samples)





