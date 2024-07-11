library(abtest)

# Honey bees experiment:
# Control group (A): 50 out of 100 times
# Experimental group (B): 65 out of 100 bees

data <- list(y1 = 50, n1 = 100, y2 = 65, n2 = 100)

prior_prob <- c(0, 0.5, 0, 0.5)
names(prior_prob) <- c("H1", "H+", "H-", "H0")

AB2 <- ab_test(
    data = data,
    prior_par = list(mu_psi = 0, sigma_psi = 1, mu_beta = 0, sigma_beta = 1),
    prior_prob = prior_prob
)

summary(AB2)

plot_posterior(AB2)
