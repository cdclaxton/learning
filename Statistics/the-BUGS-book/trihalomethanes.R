# Example 3.3.3: Trihalomethanes in tap water
#
# Prior: mu = 120 uG/L, std = 10 uG/L (Normal distribution)
# Observations: 128 uG/L, 132 uG/L -- known std = 5 uG/L (Normal dist.)

library(rjags)

# Specify the model and save to a file
model.string <- "
model {
  # Prior
  s <- 10               # standard deviation
  prec <- 1/(s * s)     # precision
  mu ~ dnorm(120, prec) # prior
  
  prec2 <- 1 / 25       # precision of the measurements
  for (i in 1:N) {
    y[i] ~ dnorm(mu, prec2)
  }
}
"
writeLines(model.string, con = "temp_model.txt")

data <- list("y" = c(128, 132), # Samples
             "N" = 2)           # Number of samples

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, 
                        variable.names = c("mu"), 
                        n.iter = 1000)
plot(samples)
summary(samples)

m <- as.matrix(samples)
hist(m[,"mu"])