# Zero-inflated Poisson distribution based outlier detection using logistic
# regression
#
#

library(tidymodels)
library(ROCit)

# ------------------------------------------------------------------------------
# Data generator
# ------------------------------------------------------------------------------

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

num_samples <- 100
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

    n_zeros_train[i] <- length(training_data[training_data == 0])
    mu_train[i] <- mean(training_data[training_data > 0])
    if (is.nan(mu_train[i])) {
        mu_train[i] <- 0
    }

    test_data <- generate_zip_samples(n_test_days, pi_test, lambda_test)

    n_zeros_test[i] <- length(test_data[test_data == 0])
    mu_test[i] <- mean(training_data[test_data > 0])
    if (is.nan(mu_test[i])) {
        mu_test[i] <- 0
    }
}

df <- data.frame(
    n_zeros_train,
    mu_train,
    n_zeros_test,
    mu_test,
    ground_truth_ratio_above_threshold
)

df$ground_truth_ratio_above_threshold <- factor(df$ground_truth_ratio_above_threshold)

# ------------------------------------------------------------------------------
# Train a logistic regression model
# ------------------------------------------------------------------------------

# Split the data into test and training
split <- initial_split(df, prop = 0.8, strata = ground_truth_ratio_above_threshold)
train <- split %>% training()
test <- split %>% testing()

model <- logistic_reg(mixture = double(1), penalty = double(1)) %>%
    set_engine("glmnet") %>%
    set_mode("classification") %>%
    fit(ground_truth_ratio_above_threshold ~ ., data = train)

tidy(model)

pred_proba <- predict(model, new_data = test, type = "prob")

probs <- pred_proba %>% pull(.pred_1)

roc_zip <- rocit(
    score = probs,
    class = test %>% pull(ground_truth_ratio_above_threshold)
)
plot(roc_zip)
