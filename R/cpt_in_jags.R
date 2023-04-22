# This R script explores how to enter a Conditional Probability Table (CPT)
# into JAGS. Inference is performed with this simple discrete Bayesian network:
#
#       Y
#     /   \
#    A     B
#
# A and B are binary inputs (0,1) and Y is governed by a CPT.
#
#   A  B  p(Y=1)
#   0  0  p_0
#   0  1  p_1
#   1  0  p_2
#   1  1  p_3

library(rjags)

# JAGS model
model_string <- "
model {
    A <- 0
    B <- 1
    Y <- cpt[A+1,B+1]
}
"

cpt <- matrix(c(
    0.2, 0.8,
    0.3, 0.7
    ), nrow = 2, byrow = TRUE)

model <- jags.model(textConnection(model_string),
    data = list(cpt = cpt))

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("Y"),
    n.iter = 20000,
    progress.bar = "none")

plot(samples)