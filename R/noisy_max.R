# Noisy Max distribution calculated using JAGS and analytically.

library(rjags)

# Find the distribution of the values of y from MCMC samples.
distribution_of_y <- function(samples) {
    m <- as.matrix(samples)
    max_y <- max(m[, "y"])

    # Calculate the distribution
    dist_y <- rep(0, max_y+1)
    for (i in 0:max_y) {
        dist_y[i+1] <- sum(m[, "y"] == i)
    }
    dist_y <- dist_y / sum(dist_y)

    return(dist_y)
}

# Noisy max with two inputs.
jags_noisy_max_two_inputs <- function(pi0, pi1) {

    # JAGS model
    model_string <- "
    model {
        # Inputs
        x0 ~ dcat(pi0)
        x1 ~ dcat(pi1)

        y <- max(x0-1, x1-1)
    }
    "

    model <- jags.model(textConnection(model_string),
        data = list(pi0 = pi0, pi1 = pi1))

    update(model, n.iter = 10000, progress.bar = "none")

    samples <- coda.samples(model,
        variable.names = c("x0", "x1", "y"),
        n.iter = 20000,
        progress.bar = "none")

    return(distribution_of_y(samples))
}

# Noisy max with three inputs.
jags_noisy_max_three_inputs <- function(pi0, pi1, pi2) {

    # JAGS model
    model_string <- "
    model {
        # Inputs
        x0 ~ dcat(pi0)
        x1 ~ dcat(pi1)
        x2 ~ dcat(pi2)

        y <- max(x0-1, x1-1, x2-1)
    }
    "

    model <- jags.model(textConnection(model_string),
        data = list(pi0 = pi0, pi1 = pi1, pi2 = pi2))

    update(model, n.iter = 10000, progress.bar = "none")

    samples <- coda.samples(model,
        variable.names = c("x0", "x1", "x2", "y"),
        n.iter = 20000,
        progress.bar = "none")

    return(distribution_of_y(samples))
}

# Find the cumulative probability function from the probability function.
cdf <- function(pdf) {

    result <- rep(0, length(pdf))
    for (i in 1:length(pdf)) {
        result[i] <- sum(pdf[1:i])
    }
    
    return(result)
}

# Find the PDF from the CDF.
pdf <- function(cdf) {

    result <- rep(0, length(cdf))
    for (i in 1:length(cdf)) {
        if (i == 1) {
            result[i] <- cdf[i]
        } else {
            result[i] <- cdf[i] - cdf[i-1]
        }
    }

    return(result)
}

# Test case
p <- c(0.1, 0.2, 0.3, 0.2, 0.2)
result <- pdf(cdf(p))
stopifnot(all.equal(p, result, 1e-5))

# Find the Noisy Max distribution analytically. Each row of the matrix m
# defines an input. Each column represents a different output state.
noisy_max <- function(m) {
    num_inputs <- dim(m)[1]  # Number of inputs to the noisy max
    num_states <- dim(m)[2]  # Number of states

    # Find the CDFs of each input
    cdfs <- matrix(0, nrow=num_inputs, ncol=num_states)
    for (i in 1:num_inputs) {
        cdfs[i,] <- cdf(m[i,])
    }

    # Initialise the output CDF
    result <- rep(0, num_states)

    # Walk through each possible output state
    for (i in 1:num_states) {
        total <- 0.0
        for (j in 1:num_inputs) {
            total <- total + log(cdfs[j, i])
        }
        result[i] <- exp(total)
    }

    # Return the PDF of the output by converting from its CDF
    return(pdf(result))
}

# Prior probability of the inputs being true
pi0 <- c(0.2, 0.3, 0.4, 0.1)
pi1 <- c(0.5, 0.4, 0.1, 0.0)

cat("Distribution using JAGS: ", jags_noisy_max_two_inputs(pi0, pi1), "\n")
cat("Analytic: ", noisy_max(matrix(c(pi0, pi1), nrow=2, byrow = TRUE)), "\n")

pi2 <- c(0.0, 0.1, 0.1, 0.8)

cat("Distribution using JAGS: ", jags_noisy_max_three_inputs(pi0, pi1, pi2), "\n")
cat("Analytic: ", noisy_max(matrix(c(pi0, pi1, pi2), nrow=3, byrow = TRUE)), "\n")

run_test_case_2 <- function(pi0, pi1) {
    jags_result <- jags_noisy_max_two_inputs(pi0, pi1)
    analytic_result <- noisy_max(matrix(c(pi0, pi1), nrow=2, byrow = TRUE))

    sse <- sum((jags_result - analytic_result)**2)
    stopifnot(sse < 1e-5)

    cat("pi0 = ", pi0, "\n")
    cat("pi1 = ", pi1, "\n")
    cat("result = ", analytic_result, "\n")
}

run_test_case_3 <- function(pi0, pi1, pi2) {
    jags_result <- jags_noisy_max_three_inputs(pi0, pi1, pi2)
    analytic_result <- noisy_max(matrix(c(pi0, pi1, pi2), nrow=3, byrow = TRUE))

    sse <- sum((jags_result - analytic_result)**2)
    stopifnot(sse < 1e-5)

    cat("pi0 = ", pi0, "\n")
    cat("pi1 = ", pi1, "\n")
    cat("pi2 = ", pi2, "\n")
    cat("result = ", analytic_result, "\n")
}

# run_test_case_2(c(0.2, 0.8), c(0.3, 0.7))
# run_test_case_2(c(0.2, 0.7, 0.1), c(0.3, 0.7, 0.0))
# run_test_case_2(c(0.2, 0.5, 0.0, 0.3), c(0.3, 0.7, 0.0, 0.0))
run_test_case_2(c(0.0, 1.0), c(0.3, 0.7))

# run_test_case_3(c(0.2, 0.8), c(0.3, 0.7), c(1.0, 0.0))

#run_test_case_3(c(0.2, 0.8, 0.0, 0.0, 0.0),
#    c(0.3, 0.6, 0.0, 0.0, 0.1), 
#    c(1.0, 0.0, 0.0, 0.0, 0.0))
