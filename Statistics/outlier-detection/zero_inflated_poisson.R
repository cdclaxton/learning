# Zero-inflated Poisson (ZIP) distribution outlier detection
#
# There is a process that generates samples that are distributed according to
# a zero-inflated Poisson distribution.
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
library(ROCit)
library(tidymodels)

# Generate n samples from a zero-inflated Poisson distribution where the
# probability of extra zeros is pi. The mean of the Poisson distribution is
# lambda.
generate_zip_samples <- function(n, pi, lambda) {
    result <- rep(0, n)
    for (i in 1:n) {
        is_zero <- rbinom(1, 1, pi)
        if (is_zero == 0) {
            result[i] <- rpois(1, lambda)
        }
    }
    return(result)
}

# Plot samples from a zero-inflated Poisson distribution
pi <- 0.3
lambda <- 10
samples <- generate_zip_samples(1000, pi, lambda)

df <- data.frame(samples)
ggplot(df, aes(x = samples)) +
    geom_histogram(binwidth = 1) +
    xlab("Value") +
    ylab("Count") +
    ggtitle("Histogram of samples from a ZIP distribution")

# ------------------------------------------------------------------------------
# Gamma distribution
# ------------------------------------------------------------------------------

# Plot a gamma distribution, which is the prior for lambda (the rate of the
# Poisson distribution), using the in-built gamma function
x <- 1:20
y <- rep(0, length(x))
for (i in x) {
    y[i] <- dgamma(i, shape = 1, rate = 0.2)
}

df <- data.frame(x, y)
ggplot(df) +
    ggtitle("Gamma distribution") +
    geom_line(aes(x = x, y = y)) +
    xlab("x") +
    ylab("p(x)")

# Plot samples from a gamma distribution using JAGS
model_string <- "
model {
    lambda1 ~ dgamma(r, lambda) # Prior of the Poisson mean
}
"

model <- jags.model(textConnection(model_string),
    data = list(
        r = 1,
        lambda = 0.2
    ),
    quiet = TRUE
)

update(model, n.iter = 10000, progress.bar = "none")

gamma_samples <- coda.samples(model,
    variable.names = c("lambda1"),
    n.iter = 20000,
    progress.bar = "none"
)

plot(gamma_samples)

# ------------------------------------------------------------------------------
# Truncated Poisson distribution
# ------------------------------------------------------------------------------

# Plot samples from a truncated distribution using JAGS
model_string <- "
model {
    y ~ dpois(lambda) T(3,)
}
"

model <- jags.model(textConnection(model_string),
    data = list(
        lambda = 2
    ),
    quiet = TRUE
)

update(model, n.iter = 10000, progress.bar = "none")

truncated_poisson_samples <- coda.samples(model,
    variable.names = c("y"),
    n.iter = 20000,
    progress.bar = "none"
)

plot(truncated_poisson_samples)

m <- as.matrix(truncated_poisson_samples)
y_samples <- unlist(m[, "y"])
cat("Minimum value of truncated Poisson =", min(y_samples), "\n")

# ------------------------------------------------------------------------------
# Bayesian inference of ZIP parameters
# ------------------------------------------------------------------------------

# JAGS model
model_string <- "
model {
    pi1 ~ dbeta(1, 1)           # Prob. of extra zeros
    lambda1 ~ dgamma(r, lambda) # Prior of the Poisson mean

    for (i in 1:N) {
        z1[i] ~ dbern(pi1)
        mu1[i] <- lambda1*(1 - z1[i])
        samples[i] ~ dpois(mu1[i])
    }
}
"

model <- jags.model(textConnection(model_string),
    data = list(
        N = length(samples),
        samples = samples,
        r = 1,
        lambda = 0.2
    ),
    quiet = TRUE
)

update(model, n.iter = 10000, progress.bar = "none")

zip_model_samples <- coda.samples(model,
    variable.names = c("pi1", "lambda1"),
    n.iter = 20000,
    progress.bar = "none"
)

plot(zip_model_samples)

# ------------------------------------------------------------------------------
# Bayesian inference using a hurdle model
# ------------------------------------------------------------------------------

# JAGS model
model_string <- "
model {
    pi ~ dbeta(1, 1)            # Prob. of extra zeros
    lambda1 ~ dgamma(r, lambda) # Prior of the Poisson mean

    for (i in 1:N_non_zero) {
        samples_non_zero[i] ~ dpois(lambda1) T(1,)
    }

    for (i in 1:N) {
        samples_0[i] ~ dbern(pi)
    }
}
"

model <- jags.model(textConnection(model_string),
    data = list(
        N = length(samples),
        samples_0 = as.integer(samples == 0),
        N_non_zero = length(samples[samples > 0]),
        samples_non_zero = samples[samples > 0],
        r = 1,
        lambda = 0.2
    ),
    quiet = TRUE
)

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("pi", "lambda1"),
    n.iter = 20000,
    progress.bar = "none"
)

plot(samples)

# ------------------------------------------------------------------------------
# Bayesian inference of rates
# ------------------------------------------------------------------------------

# Calculate the probability that the ratio of the rate of events is above the
# the threshold using a zero-inflated Poisson model. This approach uses
# independent estimates of pi and lambda as opposed to placing a distribution
# over the ratio of the rates.
p_ratio_above_threshold_zip <- function(training_data, test_data, threshold) {
    # JAGS model
    model_string <- "
    model {
        # Training model
        pi1 ~ dbeta(1, 1)           # Prob. of extra zeros
        lambda1 ~ dgamma(r, lambda) # Prior of the Poisson mean

        for (i in 1:N_train) {
            z1[i] ~ dbern(pi1)
            mu1[i] <- lambda1*(1 - z1[i])+ 0.00001
            train[i] ~ dpois(mu1[i])
        }

        # Test model
        pi2 ~ dbeta(1, 1)           # Prob. of extra zeros
        lambda2 ~ dgamma(r, lambda) # Prior of the Poisson mean

        for (i in 1:N_test) {
            z2[i] ~ dbern(pi2)
            mu2[i] <- lambda2*(1 - z2[i])+ 0.00001
            test[i] ~ dpois(mu2[i])
        }

        # Ratio
        ratio <- ((1 - pi2) * lambda2) / ((1 - pi1) * lambda1)
    }
    "

    model <- jags.model(textConnection(model_string),
        data = list(
            N_train = length(training_data),
            train = training_data,
            N_test = length(test_data),
            test = test_data,
            r = 1,
            lambda = 0.2
        ),
        quiet = TRUE
    )

    update(model, n.iter = 10000, progress.bar = "none")

    samples <- coda.samples(model,
        variable.names = c("pi1", "lambda1", "pi2", "lambda2", "ratio"),
        n.iter = 20000,
        progress.bar = "none"
    )

    m <- as.matrix(samples)
    ratio_samples <- unlist(m[, "ratio"])
    p_above_alerting_threshold <- sum(ratio_samples > threshold) /
        length(ratio_samples)

    return(p_above_alerting_threshold)
}

# Calculate the probability that the ratio of the rate of events is above the
# the threshold using a Poisson hurdle model
p_ratio_above_threshold_hurdle <- function(training_data, test_data, threshold) {
    # JAGS model
    model_string <- "
    model {
        # Training model
        pi1 ~ dbeta(1, 1)           # Prob. of extra zeros
        lambda1 ~ dgamma(r, lambda) # Prior of the Poisson mean

        for (i in 1:N_train_samples_non_zero) {
            train_samples_non_zero[i] ~ dpois(lambda1) T(1,)
        }

        for (i in 1:N_train_samples_0) {
            train_samples_0[i] ~ dbern(pi1)
        }

        # Test model
        pi2 ~ dbeta(1, 1)           # Prob. of extra zeros
        lambda2 ~ dgamma(r, lambda) # Prior of the Poisson mean

        for (i in 1:N_test_samples_non_zero) {
            test_samples_non_zero[i] ~ dpois(lambda2) T(1,)
        }

        for (i in 1:N_test_samples_0) {
            test_samples_0[i] ~ dbern(pi2)
        }

        # Ratio
        exp_train <- (1 - pi1) * lambda1 / (1 - exp(-lambda1))
        exp_test <- (1 - pi2) * lambda2 / (1 - exp(-lambda2))
        ratio <- exp_test / exp_train
    }
    "

    train_samples_non_zero <- training_data[training_data > 0]
    train_samples_0 <- as.integer(training_data == 0)

    test_samples_non_zero <- test_data[test_data > 0]
    test_samples_0 <- as.integer(test_data == 0)

    model <- jags.model(textConnection(model_string),
        data = list(
            N_train_samples_non_zero = length(train_samples_non_zero),
            train_samples_non_zero = train_samples_non_zero,
            N_train_samples_0 = length(train_samples_0),
            train_samples_0 = train_samples_0,
            N_test_samples_non_zero = length(test_samples_non_zero),
            test_samples_non_zero = test_samples_non_zero,
            N_test_samples_0 = length(test_samples_0),
            test_samples_0 = test_samples_0,
            r = 1,
            lambda = 0.2
        ),
        quiet = TRUE
    )

    update(model, n.iter = 10000, progress.bar = "none")

    samples <- coda.samples(model,
        variable.names = c("pi1", "lambda1", "pi2", "lambda2", "ratio"),
        n.iter = 20000,
        progress.bar = "none"
    )

    m <- as.matrix(samples)
    ratio_samples <- unlist(m[, "ratio"])
    p_above_alerting_threshold <- sum(ratio_samples > threshold) /
        length(ratio_samples)

    return(p_above_alerting_threshold)
}

# Calculate the probability that the ratio of the rate of events is above the
# the threshold using a Poisson model
p_ratio_above_threshold_poisson <- function(training_data, test_data, threshold) {
    model_string <- "
    model {
        lambda1 ~ dgamma(r, lambda) # Prior of the Poisson mean
        for (i in 1:N_train) {
            train[i] ~ dpois(lambda1)
        }

        lambda2 ~ dgamma(r, lambda) # Prior of the Poisson mean
        for (i in 1:N_test) {
            test[i] ~ dpois(lambda2)
        }

        ratio <- lambda2 / lambda1
    }
"

    model <- jags.model(textConnection(model_string),
        data = list(
            N_train = length(training_data),
            train = training_data,
            N_test = length(test_data),
            test = test_data,
            r = 1,
            lambda = 0.2
        ),
        quiet = TRUE
    )

    update(model, n.iter = 10000, progress.bar = "none")

    samples <- coda.samples(model,
        variable.names = c("lambda1", "lambda2", "ratio"),
        n.iter = 20000,
        progress.bar = "none"
    )

    m <- as.matrix(samples)
    ratio_samples <- unlist(m[, "ratio"])
    p_above_alerting_threshold <- sum(ratio_samples > threshold) /
        length(ratio_samples)

    return(p_above_alerting_threshold)
}

# ------------------------------------------------------------------------------
# Train a logistic regression model
# ------------------------------------------------------------------------------

train_logistic_regression <- function() {
    num_samples <- 10000
    threshold <- 1.1
    n_training_days <- 90
    n_test_days <- 30

    n_zeros_train <- rep(0, num_samples)
    mu_train <- rep(0, num_samples)
    n_zeros_test <- rep(0, num_samples)
    mu_test <- rep(0, num_samples)
    ground_truth_ratio <- rep(0, num_samples)
    ground_truth_ratio_above_threshold <- rep(0, num_samples)

    for (i in 1:num_samples) {
        pi_train <- runif(1, 0, 1) # Prob. of extra zeros
        lambda_train <- runif(1, 1, 10) # Mean of Poisson distribution

        pi_test <- runif(1, 0, 1)
        lambda_test <- runif(1, 1, 10)

        # delta <- 0.10
        # pi_test <- max(min(pi_train * runif(1, 1.0 - delta, 1.0 + delta), 1), 0)
        # lambda_test <- max(lambda_train * runif(1, 1.0 - delta, 1.0 + delta), 0)

        ground_truth_ratio[i] <- ((1 - pi_test) * lambda_test) /
            ((1 - pi_train) * lambda_train)
        ground_truth_ratio_above_threshold[i] <- ground_truth_ratio[i] > threshold

        training_data <- generate_zip_samples(
            n_training_days,
            pi_train,
            lambda_train
        )

        n_zeros_train[i] <- length(training_data[training_data == 0])
        mu_train[i] <- mean(training_data[training_data > 0])

        test_data <- generate_zip_samples(n_test_days, pi_test, lambda_test)

        n_zeros_test[i] <- length(test_data[test_data == 0])
        mu_test[i] <- mean(training_data[test_data > 0])
    }

    df <- data.frame(
        n_zeros_train,
        mu_train,
        n_zeros_test,
        mu_test,
        ground_truth_ratio_above_threshold
    )

    df$ground_truth_ratio_above_threshold <- factor(df$ground_truth_ratio_above_threshold)

    model <- logistic_reg(mixture = double(1), penalty = double(1)) %>%
        set_engine("glmnet") %>%
        set_mode("classification") %>%
        fit(ground_truth_ratio_above_threshold ~ ., data = df)

    tidy(model)
    return(model)
}

logistic_regression_model <- train_logistic_regression()

# ------------------------------------------------------------------------------
# Simulator
# ------------------------------------------------------------------------------

n_training_days <- 90
n_test_days <- 30
num_experiments <- 1000
threshold <- 1.1

ground_truth_ratio <- rep(0, num_experiments)
ground_truth_ratio_above_threshold <- rep(FALSE, num_experiments)

prob_above_threshold_zip <- rep(0, num_experiments)
prob_above_threshold_hurdle <- rep(0, num_experiments)
prob_above_threshold_poisson <- rep(0, num_experiments)
prob_above_threshold_log_reg <- rep(0, num_experiments)

for (i in 1:num_experiments) {
    if (i %% 10 == 0) {
        cat("Running experiment", i, "of", num_experiments, "\n")
    }

    pi_train <- runif(1, 0, 1) # Prob. of extra zeros
    lambda_train <- runif(1, 1, 10) # Mean of Poisson distribution

    delta <- 0.10
    pi_test <- max(min(pi_train * runif(1, 1.0 - delta, 1.0 + delta), 1), 0)
    lambda_test <- max(lambda_train * runif(1, 1.0 - delta, 1.0 + delta), 0)

    ground_truth_ratio[i] <- ((1 - pi_test) * lambda_test) /
        ((1 - pi_train) * lambda_train)
    ground_truth_ratio_above_threshold[i] <- ground_truth_ratio[i] > threshold

    training_data <- generate_zip_samples(
        n_training_days,
        pi_train,
        lambda_train
    )

    test_data <- generate_zip_samples(n_test_days, pi_test, lambda_test)

    prob_above_threshold_zip[i] <- p_ratio_above_threshold_zip(
        training_data,
        test_data,
        threshold
    )

    prob_above_threshold_hurdle[i] <- p_ratio_above_threshold_hurdle(
        training_data,
        test_data,
        threshold
    )

    prob_above_threshold_poisson[i] <- p_ratio_above_threshold_poisson(
        training_data,
        test_data,
        threshold
    )

    # Build the feature vector for the logistic regression model
    n_zeros_train <- length(training_data[training_data == 0])
    mu_train <- mean(training_data[training_data > 0])
    if (is.nan(mu_train)) {
        mu_train <- 0
    }

    n_zeros_test <- length(test_data[test_data == 0])
    mu_test <- mean(training_data[test_data > 0])
    if (is.nan(mu_test)) {
        mu_test <- 0
    }

    df_log_reg <- data.frame(
        n_zeros_train,
        mu_train,
        n_zeros_test,
        mu_test
    )

    pred_proba <- predict(logistic_regression_model,
        new_data = df_log_reg, type = "prob"
    )
    probs <- pred_proba %>% pull(.pred_1)
    prob_above_threshold_log_reg[i] <- probs[1]
    if (is.nan(probs[1])) {
        print(df_log_reg)
    }
}

df <- data.frame(
    ground_truth_ratio,
    ground_truth_ratio_above_threshold,
    prob_above_threshold_zip,
    prob_above_threshold_hurdle,
    prob_above_threshold_poisson,
    prob_above_threshold_log_reg
)
df$ground_truth_ratio_above_threshold <- factor(df$ground_truth_ratio_above_threshold)

ggplot(df) +
    geom_point(aes(x = ground_truth_ratio, y = prob_above_threshold_zip, color = "ZIP model")) +
    geom_point(aes(x = ground_truth_ratio, y = prob_above_threshold_hurdle, color = "Hurdle model")) +
    geom_point(aes(x = ground_truth_ratio, y = prob_above_threshold_poisson, color = "Poisson model")) +
    xlab("Ground truth ratio (from population)") +
    ylab("Probability ratio is above threshold")

# ------------------------------------------------------------------------------
# Plot ROC curves
# ------------------------------------------------------------------------------

roc_zip <- rocit(
    score = df$prob_above_threshold_zip,
    class = df$ground_truth_ratio_above_threshold
)
cat("ZIP model AUC =", roc_zip$AUC, "\n")

roc_hurdle <- rocit(
    score = df$prob_above_threshold_hurdle,
    class = df$ground_truth_ratio_above_threshold
)
cat("Hurdle model AUC =", roc_hurdle$AUC, "\n")

roc_poisson <- rocit(
    score = df$prob_above_threshold_poisson,
    class = df$ground_truth_ratio_above_threshold
)
cat("Poisson model AUC =", roc_poisson$AUC, "\n")

roc_log_reg <- rocit(
    score = df$prob_above_threshold_log_reg,
    class = df$ground_truth_ratio_above_threshold
)
cat("Logistic regression model AUC =", roc_log_reg$AUC, "\n")

plot(roc_zip,
    col = c(1, "gray50"),
    legend = FALSE, YIndex = FALSE
)
lines(roc_hurdle$TPR ~ roc_hurdle$FPR,
    col = 2, lwd = 2
)
lines(roc_poisson$TPR ~ roc_poisson$FPR,
    col = 3, lwd = 2
)
lines(roc_log_reg$TPR ~ roc_log_reg$FPR,
    col = 4, lwd = 2
)
legend("bottomright",
    col = c(1, 2, 3, 4),
    c(
        "ZIP model",
        "Hurdle model",
        "Poisson model",
        "Logistic regresssion model"
    ), lwd = 2
)
