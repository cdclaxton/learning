# Example 2.1.2 Coins
# Simulating data using JAGS.
#
# Y ~ Binomial(0.5, 8)
# What is Pr(Y <= 2)?

library(rjags)

# Specify the model and save to a file
model.string <- "
  model {
    Y ~ dbin(0.5, 8)
    P2 <- step(2.5 - Y)
  }
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list("Y" = 1)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = list(),
                    inits = inits, n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("Y", "P2"), n.iter = 1000)
plot(samples)

m <- as.matrix(samples)
hist(m[,"Y"])