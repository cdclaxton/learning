# This probabilistic model explores a softened version of this equation:
#
#   x = (a + b) * c
#
# where a, b and c only take on limited values, specifically:
#
#   0, 0.5, 1, 2, 4, 8, 16

library(rjags)

# JAGS model
model_string <- "
model {
    values <- c(0, 0.5, 1, 2, 4, 8, 16)

    m1 ~ dcat(pi)
    a <- values[m1]

    m2 ~ dcat(pi)
    b <- values[m2]

    m3 ~ dcat(pi)
    c <- values[m3]

    x <- (a+b) * c
}
"
 

model <- jags.model(textConnection(model_string),
    data = list(pi=c(1,1,1,1,1,1,1)))

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("x"),
    n.iter = 20000,
    progress.bar = "none")

plot(samples)
