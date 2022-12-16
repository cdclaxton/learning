# There is a unknown number of people, but the number is bounded.
# Each person can be assigned to one of a small number of groups.
#
# A Dirichlet distribution could be used as the prior, but it might be
# different to parameterise in a meaningful way.

library(rjags)

model_string <- "
model {

    # Proportion assigned to each category
    pi ~ ddirich(alpha)

    # n is the number of people
    x ~ dmulti(pi, n)
}
"

model <- jags.model(textConnection(model_string),
    data = list(alpha = c(10, 2, 30), n = 30))

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("x"),
    n.iter = 20000,
    progress.bar = "none")

plot(samples)

m <- as.matrix(samples)
