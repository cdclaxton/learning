library(bayesAB)

# Honey bees experiment:
# Control group (A): 50 out of 100 times
# Experimental group (B): 65 out of 100 bees

# Uninformative uniform prior
groupA <- sample(c(rep(0, 50), rep(1, 50)))
groupB <- sample(c(rep(0, 35), rep(1, 65)))

result <- bayesTest(groupA, groupB,
    priors = c("alpha" = 1, "beta" = 1),
    n_samples = 1e5, distribution = "bernoulli"
)

summary(result)
plot(result)
