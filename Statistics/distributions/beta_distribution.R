# Beta distribution
# ==============================================================================

library(rjags)

# Specify the model and save to a file
model.string <- "
model {
  x ~ dbeta(alpha, beta)
}
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list()

# Data
data <- list(alpha = 2, beta = 2)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 1000)
update(model, n.iter = 100)
samples <- coda.samples(model, 
                        variable.names = c("x"),
                        n.iter = 5000)
plot(samples)
summary(samples)
