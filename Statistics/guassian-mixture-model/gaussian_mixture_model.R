# Gaussian mixture model

library(rjags)

# Generate data by sampling from two Gaussian distributions
m1.true <- 100
N1 <- 200
m2.true <- 145
N2 <- 100
sd.true <- 15
y1 <- rnorm(N1, mean = m1.true, sd = sd.true)
y2 <- rnorm(N2, mean = m2.true, sd = sd.true)
y <- c(y1, y2)
N <- length(y)

hist(y)

# Specify the model and save to a file
model.string <- "
model {
  # Likelihood (N observations)
  for (i in 1:N) {
    y[i] ~ dnorm(mu[i], tau)
    mu[i] <- muOfCluster[cluster[i]]
    cluster[i] ~ dcat(pCluster[1:NCluster])
  }

  # Prior
  tau ~ dgamma(0.01, 0.01)
  for (i in 1:NCluster) {
    muOfCluster[i] ~ dnorm(0, 1e-10)
  }
  pCluster[1:NCluster] ~ ddirch(onesRepNCluster)
}
"
writeLines(model.string, con = "temp_model.txt")

# Must have at least one data point with a fixed assignment to each cluster
# otherwise some clusters will end up empty
NCluster <- 2
cluster <- rep(NA, N)
#cluster[which.min(y)] = 1  # assign the smallest value to cluster 1
#cluster[which.max(y)] = 2  # assign the largest value to cluster 2

# Initialisation
inits <- list("k" = 1)

# Data
data <- list(y = y, 
             N = N, 
             NCluster = NCluster, 
             cluster = cluster,
             onesRepNCluster = rep(1,NCluster))

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("muOfCluster", "pCluster"), n.iter = 1000)
plot(samples)
summary(samples)