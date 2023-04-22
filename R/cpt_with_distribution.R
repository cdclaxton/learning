# CPT with a distribution (as opposed to discrete values).
#
# The following CPT will be used:
#
# X_1  X_0  Y
#  0    0   p_0
#  0    1   p_1
#  1    0   p_2
#  1    1   p_3
#
# where each p_i is a categorical distribution.

library(rjags)

# JAGS model
model_string <- "
model {
    # Inputs
    x0 ~ dbern(p_x0)
    x1 ~ dbern(p_x1)

    # Get the row from the CPT
    row <- 2*x1 + x0 + 1
    pi <- cpt[row,1:2]

    # Output
    y ~ dcat(pi)
}
"

# Prior probability of the inputs being true
p_x0 <- 0.1
p_x1 <- 0.7

cpt <- matrix(c(
        0.2, 0.8,  # x1 = 0, x0 = 0
        0.3, 0.7,  # x1 = 0, x0 = 1
        0.6, 0.4,  # x1 = 1, x0 = 0
        0.1, 0.9), # x1 = 1, x0 = 1
        nrow = 4, byrow = TRUE)

# x1 x0
xs <- matrix(c(
    0, 0,
    0, 1,
    1, 0,
    1, 1),
    nrow = 4, byrow = TRUE)

model <- jags.model(textConnection(model_string),
    data = list(cpt = cpt, p_x0 = p_x0, p_x1 = p_x1))

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("x0", "x1", "y"),
    n.iter = 20000,
    progress.bar = "none")

print(summary(samples))

plot(samples)

# Calculate the distribution analytically
y_dist <- rep(0, ncol(cpt))

for (k in 1:ncol(cpt)) {  # Walk through each possible state
    total <- 0.0
    for (i in 1:nrow(cpt)) {  # Walk through each row in the CPT
        p_x0_prime <- (xs[i, 2] * p_x0) + ((1 - xs[i, 2]) * (1 - p_x0))
        p_x1_prime <- (xs[i, 1] * p_x1) + ((1 - xs[i, 1]) * (1 - p_x1))

        total <- total + p_x0_prime * p_x1_prime * cpt[i, k]
    }
    y_dist[k] <- total
}

# Calculate the distribution emphircally
y_dist_emp <- rep(0, ncol(cpt))
for (i in 1:ncol(cpt)) {
    y_dist_emp[i] <- sum(as.matrix(samples[, "y"]) == i)
}
y_dist_emp <- y_dist_emp / sum(y_dist_emp)

print(y_dist)
print(y_dist_emp)