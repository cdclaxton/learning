# Estimation of the mean of a Poisson distribution

library(rjags)

# Generate the observations
lam <- 1.2
N <- 100
obs <- rpois(N, lam)

print(obs)

# JAGS model
model_string <- "
model {
    lam ~ dgamma(3, 1)  # Prior

    for (i in 1:N) {
        p[i] ~ dpois(lam)  # Likelihood
    }
}
"

model <- jags.model(textConnection(model_string),
    data = list(p = obs, N = length(obs)))

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("lam"),
    n.iter = 20000,
    progress.bar = "none")

plot(samples)
mean_lam <- mean(as.matrix(samples)[, "lam"])

cat(paste0("Actual value of lambda: ", lam, "\n"))
cat(paste0("Esimtated value of lambda: ", mean_lam, "\n"))
