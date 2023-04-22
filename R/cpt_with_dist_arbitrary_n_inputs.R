# CPT with a distribution
#
# The CPT has an arbitrary number of inputs, with a minimum of one.

library(rjags)

# Number of inputs to the CPT
n_inputs <- 3

# Number of output states
n_states <- 5

# Make a random CPT with the required number of inputs
make_cpt <- function(n_inputs, n_states) {
    stopifnot(n_inputs > 0)
    stopifnot(n_states > 0)

    # Create an empty CPT of zeros
    n_rows <- 2**n_inputs
    cpt <- matrix(0, nrow=2**n_inputs, ncol=n_states)

    # Generate a random probability distribution for each row
    for (row_idx in 1:n_rows) {
        unnormalised <- runif(n_states, 0, 1)
        cpt[row_idx, 1:n_states] <- unnormalised / sum(unnormalised)
    }

    return(cpt)
}

# Make a random CPT
cpt <- make_cpt(n_inputs, n_states)

# Probability of each input
p <- runif(n_inputs, 0, 1)

# JAGS model
model_string <- "
model {
    # Sample the input state
    for (i in 1:N) {
        x[i] ~ dbern(p[i])
    }

    # Get the row from the CPT
    for (i in 1:N) {
        row_i[i] <- 2**(i-1) * x[i]
    }
    row <- round(sum(row_i) + 1)

    # Probability from CPT
    pi <- cpt[row, 1:M]

    # Output
    y ~ dcat(pi)
}
"

model <- jags.model(textConnection(model_string),
    data = list(p=p, cpt=cpt, N=n_inputs, M=n_states))

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("y"),
    n.iter = 20000,
    progress.bar = "none")

# Calculate the distribution from the samples
y_dist_samples <- rep(0, n_states)
m <- as.matrix(samples[, "y"])
for (i in 1:n_states) {
    y_dist_samples[i] <- sum(m == i)
}
y_dist_samples <- y_dist_samples / sum(y_dist_samples)
print(y_dist_samples)

# input_idx and row_idx are assumed to start at 0.
state <- function(row_idx, input_idx) {
    x <- 2**input_idx
    st <- bitwAnd(row_idx, x) > 0

    if (!(st == 1 || st == 0)) {
        stop("State (", st, ") is invalid. row_idx = ", 
            row_idx, ", input_idx = ", input_idx)
    }
    return(st)
}

# Calculate the expected distribution analytically
y_dist_analytical <- rep(0, n_states)
for (k in 1:n_states) {
    total <- 0.0

    for (i in 1:nrow(cpt)) {
        x <- cpt[i, k]
        for (j in 1:n_inputs) {
            s <- state(i-1, j-1)
            p_prime <- (s * p[j]) + ((1 - s) * (1 - p[j]))
            stopifnot(p_prime >= 0.0 && p_prime <= 1.0)
            x <- x * p_prime
        }
        total <- total + x
    }

    y_dist_analytical[k] <- total
}

print(y_dist_analytical)
