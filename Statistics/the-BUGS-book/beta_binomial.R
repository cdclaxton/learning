# Example 2.7.1: Surgery prediction
# Beta-binomial

library(rjags)

# Specify the model and save to a file
model.string <- "
model {
  theta ~ dbeta(3, 27)  # prior distribution
  Y ~ dbin(theta, 20)   # sampling distribution
  P6 <- step(Y - 5.5)   # =1 if y >= 6, 0 otherwise
}
"
writeLines(model.string, con = "temp_model.txt")

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = list(),
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("Y", "P6"), n.iter = 1000)
plot(samples)
summary(samples)
