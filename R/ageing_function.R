library(functional)

# Time range (in days)
time <- 0:60

# Sigmoid function for a given time x.
sigmoid <- function(x, a, b) {
    1 / (1 + exp(a * (x - b)))
}

# Constant decay for a given time x.
constant <- function(x) {
    1.0
}

lowToHigh <- function(x, t) {
    (x > t) * 1.0
}

highToLow <- function(x, t) {
    (x < t) * 1.0
}

# Probability of the input (event) given a range of times, the time
# of the event and a probability decay function.
prob_of_input <- function(time, time_of_event, decay_fn) {
    y = rep(0, length(time))
    for (idx in 1:length(time)) {
        if (time[idx] >= time_of_event) {
            y[idx] <- decay_fn(time[idx] - time_of_event)
        } else {
            y[idx] <- 0
        }
    }
    y
}

# Simple Bayesian network
# 
# i1 --->  |----|
#          |    |
# i2 --->  | n1 |  ---> r1
#          |    |
# i3 --->  |----|
#
# Input i has a probability p(i)
# CPT for node n1 defines probabilities p(r1|i1, i2, i3)
# Required: marginal probability p(r1)
#
# The joint probability is given by:
#
#   p(i1,i2,i3,r1) = p(r1|i1,i2,i3) * p(i1) * p(i2) * p(i3)
#
# The marginal probability p(r1) is given by:
#
#   p(r1) = sum_{i1} sum_{i2} sum_{i3} p(r1|i1,i2,i3) * p(i1) * p(i2) * p(i3)
#
# The CPT is defined using the Noisy OR model given by:
#
#   p(r1|i1,i2,i3) = 1 - (1-q)^i1 * (1-q)^i2 * (1-q)^i3
#
# where q is the probability that a single input causes the 
# output to be true.

# CPT function
prob_r1_given_i <- function(q, i1, i2, i3) {
    1 - (1 - q)^i1 * (1 - q)^i2 * (1 - q)^i3
}

# Marginal probability p(r1).
prob_r1 <- function(q, p_i1, p_i2, p_i3) {
    total <- 0

    for (i1_prime in 0:1) {

        p_i1_prime <- (p_i1 ^ i1_prime) * ((1 - p_i1)^(1 - i1_prime))

        for (i2_prime in 0:1) {

            p_i2_prime <- (p_i2 ^ i2_prime) * (1 - p_i2)^(1 - i2_prime)

            for (i3_prime in 0:1) {

                p_i3_prime <- (p_i3 ^ i3_prime) * (1 - p_i3)^(1 - i3_prime)

                total <- total + prob_r1_given_i(q, i1_prime, i2_prime, i3_prime) * 
                    p_i1_prime * p_i2_prime * p_i3_prime
            }
       }
    }

    total
}

# Marginal probability p(r1) as a function of time.
p_r1_over_time <- function(time, q, t1, t2, t3, decay_fn) {
    y <- rep(0, length(time))
    for (idx in 1:length(time)) {
        # Probability of the inputs
        pi1 <- prob_of_input(time[idx], t1, decay_fn)
        pi2 <- prob_of_input(time[idx], t2, decay_fn)
        pi3 <- prob_of_input(time[idx], t3, decay_fn)

        # Calculate marginal probability p(r1)
        y[idx] <- prob_r1(q, pi1, pi2, pi3)
    }

    y
}

emergence_multiple_events <- function(time, q, t1, t2, t3, decay_fn1, decay_fn2) {
    p_r1_over_time(time, q, t1, t2, t3, decay_fn1) -
        p_r1_over_time(time, q, t1, t2, t3, decay_fn2)
}

# Emergence for a single event, i.e. no Bayesian network.
emergence_single_event <- function(time, time_of_event, decay_fn1, decay_fn2) {
    prob_of_input(time, time_of_event, decay_fn1) -
        prob_of_input(time, time_of_event, decay_fn2)
}

# Emergence of a single event
par(mfrow = c(4, 3))

# Confidence with no decay
plot(time, p_r1_over_time(time, 0.7, 0, 0, 0, constant),
    xlab = "Time", ylab = "Probability", main = "Three events at time 0",
    ylim = c(0, 1))
plot(time, p_r1_over_time(time, 0.7, 0, 10, 20, constant),
    xlab = "Time", ylab = "Probability", main = "Three events at time 0, 10, 20",
    ylim = c(0, 1))
plot(time, p_r1_over_time(time, 0.7, 5, 10, 40, constant),
    xlab = "Time", ylab = "Probability", main = "Three events at time 5, 10, 40",
    ylim = c(0, 1))

# Confidence with sigmoid decay
sigmoid_decay <- Curry(sigmoid, a = 1, b = 7)
plot(time, p_r1_over_time(time, 0.7, 0, 0, 0, sigmoid_decay),
    xlab = "Time", ylab = "Probability", main = "Three events at time 0",
    ylim = c(0, 1))
plot(time, p_r1_over_time(time, 0.7, 0, 10, 20, sigmoid_decay),
    xlab = "Time", ylab = "Probability", main = "Three events at time 0, 10, 20",
    ylim = c(0, 1))
plot(time, p_r1_over_time(time, 0.7, 5, 10, 40, sigmoid_decay),
    xlab = "Time", ylab = "Probability", main = "Three events at time 5, 10, 40",
    ylim = c(0, 1))

# Emergence of constant - decayed version
decay_fn1 <- constant
decay_fn2 <- Curry(sigmoid, a = -1, b = 7)

plot(time, emergence_multiple_events(time, 0.7, 0, 0, 0, decay_fn1, decay_fn2),
    xlab = "Time", ylab = "Emergence", main = "Three events at time 0",
    ylim = c(0, 1))

plot(time, emergence_multiple_events(time, 0.7, 0, 10, 20, decay_fn1, decay_fn2),
    xlab = "Time", ylab = "Emergence", main = "Three events at time 0, 10, 20",
    ylim = c(0, 1))

plot(time, emergence_multiple_events(time, 0.7, 5, 20, 40, decay_fn1, decay_fn2),
    xlab = "Time", ylab = "Emergence", main = "Three events at time 5, 20, 40",
    ylim = c(0, 1))

# Emergence of recent - old
decay_fn1 <- Curry(highToLow, t = 7)
decay_fn2 <- Curry(lowToHigh, t = 7)

plot(time, emergence_multiple_events(time, 0.7, 0, 0, 0, decay_fn1, decay_fn2),
    xlab = "Time", ylab = "Emergence", main = "Three events at time 0",
    ylim = c(-1, 1))

plot(time, emergence_multiple_events(time, 0.7, 0, 10, 20, decay_fn1, decay_fn2),
    xlab = "Time", ylab = "Emergence", main = "Three events at time 0, 10, 20",
    ylim = c(-1, 1))

plot(time, emergence_multiple_events(time, 0.7, 5, 20, 40, decay_fn1, decay_fn2),
    xlab = "Time", ylab = "Emergence", main = "Three events at time 5, 20, 40",
    ylim = c(-1, 1))