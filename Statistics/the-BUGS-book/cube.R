# Example 2.4.1 Cube
# Transformation of a random variable.

library(rjags)

# Specify the model and save to a file
model.string <- "
  model {
    Z ~ dnorm(0, 1)
    Y <- pow(2*Z + 1, 3)
    P10 <- step(Y - 10)
  }
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list("Z" = 0.5)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = list(),
                    inits = inits, n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("Z", "Y", "P10"), n.iter = 1000)
plot(samples)
summary(samples)