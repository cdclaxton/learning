# Gamma distribution
# ==============================================================================

library(rjags)

# Specify the model and save to a file
model.string <- "
model {
  x ~ dgamma(shape, rate)
}
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list()

# Data
data <- list(shape = 1, rate = 0.5)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 1000)
update(model, n.iter = 100)
samples <- coda.samples(model, 
                        variable.names = c("x"),
                        n.iter = 5000)
plot(samples)
summary(samples)
