# Suppose there are no events in N days, e.g. N = 90.
# In an M = 5 day period there are two events. How likely is it that those two
# events would occur if the underlying generating process doesn't change?

library(rjags)

model_string <- "
model {
    theta ~ dunif(0, 1)  # (prior) probability of an event on a given day
    c ~ dbinom(theta, N) # number of events in the learning phase
    t ~ dbinom(theta, M) # number of events in the test phase
}
"

model <- jags.model(textConnection(model_string),
    data = list(N = 90, c = 0, M = 5)
)

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("theta", "t"),
    n.iter = 20000,
    progress.bar = "none"
)

plot(samples)

m <- as.matrix(samples)
p <- sum(unlist(samples[, "t"]) == 2) / nrow(m)
cat(paste0("Probability of 2 events = ", p, "\n"))
