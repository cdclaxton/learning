# Categorical distribution

library(rjags)

# JAGS model
model_string <- "
model {
    x ~ dcat(pi)
}
"

pi <- c(0.4, 0.2, 0.3, 0.1)

model <- jags.model(textConnection(model_string),
    data = list(pi = pi))

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("x"),
    n.iter = 20000,
    progress.bar = "none")

summary(samples)

plot(samples)
