# Multinomial distribution

library(rjags)

# JAGS model
model_string <- "
model {
    x ~ dmulti(pi[1:N], 1)
}
"

pi <- c(0.4, 0.2, 0.3, 0.1)
N <- 4

model <- jags.model(textConnection(model_string),
    data = list(pi = pi, N = N))

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("x"),
    n.iter = 20000,
    progress.bar = "none")

for (idx in 1:N) {
    mu <- mean(as.matrix(samples[, idx]))
    cat(paste0("Actual: ", pi[idx], ", Expected: ", mu, "\n"))
}
