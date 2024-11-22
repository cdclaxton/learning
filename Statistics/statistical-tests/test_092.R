library(survival)

sample <- list(
    time = c(3, 3, 3, 4, 3, 1, 1, 2, 2, 3, 3, 4),
    status = c(0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1),
    factor.1 = c(2, 2, 1, 0, 2, 1, 1, 1, 0, 0, 0, 0),
    factor.2 = c(1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1)
)

fit <- coxph(Surv(time, status) ~ factor.1 + factor.2, sample)
fit

# p=0.8288 > 0.05 => cannot reject null hypothesis of proportionality
cox.zph(fit)
