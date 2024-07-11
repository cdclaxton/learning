# Dirchlet distribution

library(rjags)

# Specify the model and save to a file
model.string <- "
model {
  p ~ ddirch(alpha)
}
"
writeLines(model.string, con = "temp_model.txt")

# Data
data <- list(alpha = c(10,1,1))

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("p"), n.iter = 1000)
plot(samples)
summary(samples)