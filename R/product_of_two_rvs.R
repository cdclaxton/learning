# Calculate the probability distribution for the product of two random numbers.

sum_to_unity <- function(p) {
    return(abs(sum(p) - 1.0) < 1e-5)
}

multinomial_sample <- function(p) {

    # Preconditions
    stopifnot(sum_to_unity(p))
    
    which(rmultinom(1, 1, p) == 1)
}

calc_product_monte_carlo <- function(p1, p2, n_samples) {

    # Preconditions
    stopifnot(length(p1) == length(p2))
    stopifnot(sum_to_unity(p1))
    stopifnot(sum_to_unity(p2))
    stopifnot(n_samples > 0)

    # Maximum value obtainable from the sum of p1 and p2
    max_value <- (length(p1) - 1) * (length(p2) - 1)

    counts <- rep(0, max_value + 1)
    for (i in 1:n_samples) {
        v1 <- multinomial_sample(p1) - 1
        v2 <- multinomial_sample(p2) - 1
        idx <- v1 * v2 + 1
        counts[idx] <- counts[idx] + 1
    }

    return(counts / sum(counts))
}   

calc_product <- function(p1, p2) {

    # Preconditions
    stopifnot(length(p1) > 0)
    stopifnot(length(p1) == length(p2))
    stopifnot(sum_to_unity(p1))
    stopifnot(sum_to_unity(p2))
    
    # Maximum value obtainable from the sum of p1 and p2
    max_value <- (length(p1) - 1) * (length(p2) - 1)

    # Vector of probabilities
    probs <- rep(0, max_value + 1)

    for (i in 1:length(p1)) {
        for (j in 1:length(p2)) {
            outcome <- (i - 1) * (j - 1)
            probs[outcome + 1] <- probs[outcome + 1] + p1[i] * p2[j]
        }
    }

    return(probs)
}

#         0    1    2    3
p1 <- c(0.1, 0.7, 0.1, 0.1)
p2 <- c(0.1, 0.5, 0.3, 0.1)

monte_carlo_result <- calc_product_monte_carlo(p1, p2, 10000)
cat("Monte carlo result: ", monte_carlo_result, "\n")

analytic_result <- calc_product(p1, p2)
cat("Analytic result:", analytic_result, "\n")

ss <- sum((monte_carlo_result - analytic_result)**2)
cat("Sum of squared error: ", ss, "\n")
