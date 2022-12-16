# Suppose a certain number of people are counted at a particular location and
# the total number of people is required. The fraction of the people counted
# is known approximately.
#
# This problem might be ill-posed.

library(rjags)

# Actual number of people
nu <- 310

# Proportion of people observed
prop <- 0.1

# Number of people observed
obs <- round(nu * prop)

# Poisson distribution with a Gamma prior
# For a large value of lambda.nu, the Poisson distribution approximates a
# discrete Gaussian distribution

model_string <- "
model {
    # Rate (nu.ra) and shape (nu.sh) of the Gamma prior
    nu.ra <- ( nu.m + sqrt( nu.m^2 + 4*nu.sd^2 )) / ( 2 * nu.sd^2 )
    nu.sh <- 1 + nu.m * nu.ra

    # Mean number of people
    lambda.nu ~ dgamma(nu.sh, nu.ra)

    # Actual number of people
    nu ~ dpois(lambda.nu)

    # Prior for the proportion of the people observed
    prop ~ dunif(0.0001, 0.3)

    # Number of people observed
    obs <- round(nu * prop)

    # The number of people observed is actually a known (deterministic) value,
    # but it can't be inferred
    obs.noise ~ dnorm(obs, 0.01)
}
"

model <- jags.model(textConnection(model_string),
    data = list(nu.m = 600, nu.sd = 400, obs.noise = obs))

update(model, n.iter = 100000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("lambda.nu", "nu", "prop", "obs.noise"),
    n.iter = 20000,
    progress.bar = "none")

plot(samples)

cat("Actual number of people:", obs, "\n")

# Summarise the results
m <- as.matrix(samples)
prop_est <- mean(m[, "prop"])
nu_est <- mean(m[, "nu"])
cat("Estimated number of people:", nu_est, "\n")
cat("Estimated proportion observed:", prop_est, "\n")
cat("Estimated number of people observed", nu_est * prop_est, "\n")
