# Poisson outlier detection
#
# There is a training window in which the mean of the distribution can be
# learnt.
#
# The test window may be longer or shorter than the training window.
#
# What is the probability that the number of events in the test window is
# greater than that expected given the training window?

library(caret)
library(ggplot2)
library(rjags)
library(ROCit)

p_ratio_above_threshold <- function(training_data, test_data, threshold) {
    model_string <- "
    model {
        lambda1 ~ dgamma(1, 2)
        for (i in 1:N_train) {
            train[i] ~ dpois(lambda1)
        }

        lambda2 ~ dgamma(1, 2)
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
            test = test_data
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

# Generate a dataset
N_training_days <- 90
N_test_days <- 30
threshold <- 1.1

num_experiments <- 100
actual_ratio <- rep(0, num_experiments)
actual_ratio_above_threshold <- rep(FALSE, num_experiments)
ground_truth_ratio <- rep(0, num_experiments)
ground_truth_ratio_above_threshold <- rep(FALSE, num_experiments)
prob_above_threshold <- rep(0, num_experiments)

for (i in 1:num_experiments) {
    lambda_train <- runif(1, 0.001, 10)
    lambda_test <- runif(1, 0.25, 2) * lambda_train

    training_data <- rpois(N_training_days, lambda_train)
    test_data <- rpois(N_test_days, lambda_test)

    train_rate <- sum(training_data) / N_training_days
    test_rate <- sum(test_data) / N_test_days
    actual_ratio[i] <- test_rate / train_rate

    if (actual_ratio[i] > threshold) {
        actual_ratio_above_threshold[i] <- TRUE
    } else {
        actual_ratio_above_threshold[i] <- FALSE
    }

    ground_truth_ratio[i] <- lambda_test / lambda_train
    if (ground_truth_ratio[i] >= threshold) {
        ground_truth_ratio_above_threshold[i] <- TRUE
    } else {
        ground_truth_ratio_above_threshold[i] <- FALSE
    }

    prob_above_threshold[i] <- p_ratio_above_threshold(
        training_data,
        test_data, threshold
    )
}

df <- data.frame(
    ground_truth_ratio,
    ground_truth_ratio_above_threshold,
    actual_ratio,
    prob_above_threshold,
    actual_ratio_above_threshold
)
df$actual_ratio_above_threshold <- factor(df$actual_ratio_above_threshold)
df$ground_truth_ratio_above_threshold <- factor(df$ground_truth_ratio_above_threshold)

ggplot(df) +
    geom_point(aes(
        x = ground_truth_ratio,
        y = prob_above_threshold,
        colour = actual_ratio_above_threshold
    ))

# Plotting the ground truth ratio (i.e. using the population lambdas) against
# the actual ratio (i.e. using the counts from the samples) gives an impression
# of the spread in the actual ratio for a ground truth ratio value.
ggplot(df) +
    geom_point(aes(x = ground_truth_ratio, y = actual_ratio))

# Plotting the ground truth ratio (i.e. using the population lambdas) against
# the probability that the ratio is above the threshold provides a visual
# indication of the correlation
ggplot(df) +
    geom_point(aes(x = ground_truth_ratio, y = prob_above_threshold)) +
    geom_vline(xintercept = threshold)

cat("Confusion matrix using a simple ratio test:\n")
confusionMatrix(
    df$actual_ratio_above_threshold,
    df$ground_truth_ratio_above_threshold
)

cat("-----\n")

ROCit_obj <- rocit(
    score = df$prob_above_threshold,
    class = df$ground_truth_ratio_above_threshold
)
p <- plot(ROCit_obj)
cutoff <- p$`optimal Youden Index point`["cutoff"]

thresholded <- rep(FALSE, num_experiments)
for (i in 1:num_experiments) {
    if (prob_above_threshold[i] >= cutoff) {
        thresholded[i] <- TRUE
    }
}
thresholded <- factor(thresholded)

cat(
    "Confusion matrix using the JAGS model with a probability threshold of ",
    cutoff, "\n"
)
confusionMatrix(thresholded, df$ground_truth_ratio_above_threshold)
