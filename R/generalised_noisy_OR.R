# Notes from http://staff.utia.cas.cz/vomlel/Voml_3484.pdf
#
# The generalised Noisy OR model allows the inputs to be multi-valued,
# ordinal, discrete variables.
#
#   X1    X2  ...  Xn
#
#    |    |         |
#    v    v         v
#
#   X1'  X2'       Xn'
#
#    |    |         |
#    |    |--> Y <--|
#    |------->
#
# The probability of Y=1 conditioned on the inputs is given by:
#
# p(Y=1 | X_1=x_1, ..., X_n=x_n) = 1 - \prod_{i=1}^{N} (p_i)^{x_i}
#
# where p_i is the inhibition probability.
#
# There is one parameter p_i for each parent X_i (no matter the number of
# values of X_i), therefore it's a restricted model.
#
# To add a leaky cause, add an auxiliary parent X_0 whose value is always 1.
#
# p_0 = p_L < 1
#
# p(Y=1 | X_1=x_1, ..., X_n=x_n) = 1 - p_L \prod_{i=1}^{N} (p_i)^{x_i}

library(rjags)

# One input
x1_values <- 0:4
p1 <- 1 - 0.6

m <- matrix(0, length(x1_values), 1)
for (x1 in x1_values) {
    m[x1 + 1, 1] <- 1 - p1^x1
}

# Two inputs
x1_values <- 0:4
p1 <- 1 - 0.6

x2_values <- 0:2
p2 <- 1 - 0.8

m <- matrix(0, length(x1_values), length(x2_values))
for (x1 in x1_values) {
    for (x2 in x2_values) {
        m[x1 + 1, x2 + 1] <- 1 - (p1^x1) * (p2^x2)
    }
}

# Three inputs
x1_values <- 0:4
p1 <- 1 - 0.6

x2_values <- 0:2
p2 <- 1 - 0.8

x3_values <- 0:3
p3 <- 1 - 0.2

m <- array(0, dim = c(length(x1_values), length(x2_values), length(x3_values)))

for (x1 in x1_values) {
    for (x2 in x2_values) {
        for (x3 in x3_values) {
            m[x1 + 1, x2 + 1, x3 + 1] <- 1 - (p1^x1) * (p2^x2) * (p3^x3)
        }
    }
}

# JAGS model with a 3-input generalised OR
model_string <- "
model {
    x1 ~ dcat(pi1)
    x2 ~ dcat(pi2)
    x3 ~ dcat(pi3)

    py <- m[x1, x2, x3]
    y ~ dbern(py)
}
"

model <- jags.model(textConnection(model_string),
    data = list(
        pi1 = c(1/5, 1/5, 1/5, 1/5, 1/5),
        pi2 = c(1/3, 1/3, 1/3),
        pi3 = c(1/4, 1/4, 1/4, 1/4),
        m = m
    ))

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("x1", "x2", "x3", "y"),
    n.iter = 20000,
    progress.bar = "none")

plot(samples)

m2 <- as.matrix(samples)[, "y"]
print(mean(m2))
