# Example 2.3.1 Simulating from a Student's t distribution

library(rjags)

# Specify the model and save to a file
model.string <- "
  model {
    Y ~ dt(10, 2, 4)
  }
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list("Y" = 10)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = list(),
                    inits = inits, n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("Y"), n.iter = 1000)
plot(samples)
summary(samples)