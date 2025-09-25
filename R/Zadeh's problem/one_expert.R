# Single expert model
library(ggplot2)

valid_probability <- function(p) {
    valid <- (0.0 <= p && p <= 1.0)
    if (valid == FALSE) {
        cat("Probability is not valid:", p)
    }
    return(valid)
}

posterior_conditional <- function(p_s, p_t_true) {
    stopifnot(valid_probability(p_s))
    stopifnot(valid_probability(p_t_true))
    
    p_s_and_t <- p_s * p_t_true
    p_not_s_and_t <- (1-p_s) *(1-p_t_true)

    p <- p_s_and_t / (p_s_and_t + p_not_s_and_t)
    stopifnot(valid_probability(p))

    return(p)
}

posterior_over_prior_range <- function(prior, p_t_true) {
    result <- rep(0, length(prior))
    for (i in 1:length(prior)) {
        result[i] = posterior_conditional(prior[i], p_t_true)
    }

    return(result)
}

prior <- seq(0, 1, 0.01)
posterior_10 <- posterior_over_prior_range(prior, 0.10)
posterior_25 <- posterior_over_prior_range(prior, 0.25)
posterior_50 <- posterior_over_prior_range(prior, 0.50)
posterior_75 <- posterior_over_prior_range(prior, 0.75)
posterior_90 <- posterior_over_prior_range(prior, 0.90)
df <- data.frame(prior, posterior_10, posterior_25, posterior_50, posterior_75, posterior_90)

p <- ggplot(df, aes(prior)) + 
    geom_line(aes(y = posterior_10, colour = "posterior_10")) +
    geom_line(aes(y = posterior_25, colour = "posterior_25")) +
    geom_line(aes(y = posterior_50, colour = "posterior_50")) + 
    geom_line(aes(y = posterior_75, colour = "posterior_75")) +
    geom_line(aes(y = posterior_90, colour = "posterior_90")) +
    xlab('Prior probability p(s)') +
    ylab('Posterior conditional p(s|t)')

png("one_expert.png")
print(p)
dev.off()