# Example 3.5.1: Heart transplants


library(rjags)

# Specify the model and save to a file
model.string <- "
model {
  yT ~ dbin(pT, nT)
  pT ~ dunif(0, 1)
  for (i in 1:8) {
    sP[i] ~ dexp(theta)
  }
  theta ~ dgamma(0.001, 0.001)
  surv.t <- pT / theta  # expected survival with transplant
  Is <- surv.t - 2  # expected lifetime without transplant
}
"
writeLines(model.string, con = "temp_model.txt")

inits = list(theta = 1)

data <- list(yT = 8,
             nT = 10,
             sP = c(2,3,4,4,6,7,10,12))

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data, inits = inits,
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, 
                        variable.names = c("Is", "pT", "surv.t"), 
                        n.iter = 1000)
plot(samples)
summary(samples)
