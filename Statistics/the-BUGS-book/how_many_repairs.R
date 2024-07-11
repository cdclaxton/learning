# Example 2.5.1 Repairs: How many trick

library(rjags)

# Specify the model and save to a file
model.string <- "
  model {
    for (i in 1:20) { Y[i] ~ dgamma(4, 0.04) }
    cum[1] <- Y[1]
    for (i in 2:20) {
      cum[i] <- cum[i-1] + Y[i]
    }
    for (i in 1:20) {
      cum.step[i] <- i * step(1000 - cum[i])
    }
    sorted.cum.step <- sort(cum.step[])
    number <- sorted.cum.step[20]
  }
"
writeLines(model.string, con = "temp_model.txt")

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = list(),
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("number"), n.iter = 1000)
plot(samples)
summary(samples)