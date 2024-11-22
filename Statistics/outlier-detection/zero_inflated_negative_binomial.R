# Zero-inflated negative binomial distribution outlier detection
#
# There is a process that generates samples that are distributed according to
# a zero-inflated negative binomial distribution.
#
# The samples represent the number of events on a given day.
#
# Data within a training window can be used to estimate the parameters of the
# distribution.
#
# The problem is to reliably detect an increase in the number of events in a
# test window.
#
# The increase in the number of events could be due to there being fewer days
# on which no events occur or an increase in the number of events on a given
# day.

library(ggplot2)
library(rjags)

# ------------------------------------------------------------------------------
# Negative binomial distribution
# ------------------------------------------------------------------------------

# Plot a negative binomial distribution
x <- 0:15
y <- rep(0, length(x))
for (i in x) {
    y[i + 1] <- dnbinom(i, 5, 0.5)
}

df <- data.frame(x, y)
ggplot(df, aes(x = x, y = y)) +
    geom_col() +
    ggtitle("Negative binomial distribution") +
    xlab("x") +
    ylab("p(x)")

# The mean of the distribution is given by r(1-p)/p. Plot the function
# (1-p)/p
x <- (1:100) / 100
y <- rep(0, length(x))
idx <- 1
for (i in x) {
    y[idx] <- (1 - i) / i
    idx <- idx + 1
}

df <- data.frame(x, y)
ggplot(df, aes(x = x, y = y)) +
    geom_line() +
    xlab("p") +
    ylab("(1-p)/p")

# Calculate the parameters of the negative binomial distribution (r, p) given
# the equivalent mean of a Poisson distribution (mu) and its overdispersion
# factor (delta).
nb_params <- function(mu, delta) {
    stopifnot(delta > 1)

    p <- 1 / delta
    r <- mu / (delta - 1)

    return(list(p = p, r = r))
}

# Plot the PDF of a negative binomial distribution given equivalent values of
# a Poisson distribution
x <- 0:40
y_nb <- rep(0, length(x))
y_po <- rep(0, length(x))
mu <- 15
delta <- 3
params1 <- nb_params(mu, delta)
for (i in x) {
    y_nb[i + 1] <- dnbinom(i, params1$r, params1$p)
    y_po[i + 1] <- dpois(i, mu)
}

df <- data.frame(x = x, "Negative binomial" = y_nb, "Poisson" = y_po)
mdf <- reshape2::melt(df, id.var = "x")

ggplot(mdf, aes(x = x, y = value, color = variable)) +
    geom_line() +
    geom_point() +
    ylab("p(x)")

# Generate samples using the parameters and check the mean and variance
samples <- rnbinom(100, params1$r, params1$p)
cat("Expected a mean of", mu, ", got", mean(samples), "\n")
cat("Expected a variance of", delta * mu, ", got", var(samples), "\n")

# ------------------------------------------------------------------------------
# Zero-inflated negative binomial distribution
# ------------------------------------------------------------------------------

# Generate samples from a zero-inflated negative binomial distribution
zinb <- function(n_samples, pi, r, p) {
    result <- rep(0, n_samples)

    # Whether the zero value is used (1) or a value from the negative binomial
    # distribution (0)
    is_zero <- rbinom(n_samples, 1, pi)

    for (i in 1:n_samples) {
        if (is_zero[i] == 0) {
            result[i] <- rnbinom(1, r, p)
        }
    }

    return(result)
}

# ------------------------------------------------------------------------------
# Bayesian inference of a zero-inflated negative binomial distribution model
# ------------------------------------------------------------------------------

# Probability that the ratio of the means is above the threshold
p_ratio_above_threshold <- function(training, test, threshold) {


}

# ------------------------------------------------------------------------------
# Experiments
# ------------------------------------------------------------------------------

n_training_days <- 90
n_test_days <- 30
num_experiments <- 1000
threshold <- 1.1

prob_ratio_above_threshold <- rep(0, num_experiments)

for (i in 1:num_experiments) {
    pi_train <- runif(1, 0, 1) # Prob. of extra zeros
    mu_train <- runif(1, 0, 50)
    delta_train <- runif(1, 1, 3)

    pi_test <- runif(1, 0, 1) # Prob. of extra zeros
}
