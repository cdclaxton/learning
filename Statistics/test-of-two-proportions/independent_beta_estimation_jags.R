# Independent beta estimation approach using JAGS
# Compares the agreement of two proportions

library(rjags)

model_string <- "
model{
    # Control group
    theta.a ~ dbeta(1, 1)
    y.a ~ dbinom(theta.a, n.a)

    # Experimental group
    theta.b ~ dbeta(1, 1)
    y.b ~ dbinom(theta.b, n.b)

    # Difference
    delta <- theta.a - theta.b
}
"

# Control group (A): 50 out of 100 times => y.a = 50, n.a = 100
# Experimental group (B): 65 out of 100 bees => y.b = 65, n.b = 100
model <- jags.model(textConnection(model_string),
    data = list(
        y.a = 50, n.a = 100,
        y.b = 65, n.b = 100
    )
)

# Burn in
update(model, 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("theta.a", "theta.b", "delta"),
    n.iter = 10000, progress.bar = "none"
)
plot(samples)

# Calculate the probability that delta > 0 from the samples
delta_samples <- unlist(samples[, "delta"])
prob_above_0 <- sum(delta_samples > 0) / length(delta_samples)

cat("Probability of (theta.a - theta.b) > 0: ", prob_above_0, "\n")
