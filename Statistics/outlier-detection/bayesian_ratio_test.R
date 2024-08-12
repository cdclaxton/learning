# N events occur in T1 days
# M events occur in T2 days
# What is the probability that the rate of events occurring has increased
# by more than 10%?

library(rjags)

model_string <- "
model {
    theta1 ~ dbeta(1, 1)
    N ~ dbinom(theta1, T1)

    theta2 ~ dbeta(1, 1)
    M ~ dbinom(theta2, T2)

    ratio <- theta2 / theta1
}
"

model <- jags.model(textConnection(model_string),
    data = list(N = 10, T1 = 90, M = 1, T2 = 30)
)

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("theta1", "theta2", "ratio"),
    n.iter = 20000,
    progress.bar = "none"
)

plot(samples)

m <- as.matrix(samples)
ratio_samples <- unlist(m[, "ratio"])
alerting_threshold <- 1.1
p_above_alerting_threshold <- sum(ratio_samples > alerting_threshold) /
    length(ratio_samples)
cat(paste0(
    "Probability of ratio above ", alerting_threshold,
    " = ", p_above_alerting_threshold, "\n"
))
