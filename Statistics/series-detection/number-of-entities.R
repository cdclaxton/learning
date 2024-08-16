library(rjags)

model_string <- "
model {
    for (i in 1:N) {
        pi[i] = 1/N
    }
    M ~ dcat(pi)  # number of entities

    for (i in 1:N) {
        v[i] ~ dunif(1, 10)
        c[i] <- ifelse(i<=M, v[i], 0)
    }
    total <- sum(c)
}
"

model <- jags.model(textConnection(model_string),
    data = list(N = 10)
)

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("M", "total"),
    n.iter = 20000,
    progress.bar = "none"
)

plot(samples)
