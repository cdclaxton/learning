library(lawstat)

ordinal.score.1 <- c(2, 2, 4, 1, 1, 4, 1, 3, 1, 5, 2, 4, 1, 1)
ordinal.score.2 <- c(3, 3, 4, 3, 1, 2, 3, 3, 1, 5, 4)

# p-value = 0.2586 > 0.05 => don't reject null hypothesis
brunner.munzel.test(ordinal.score.1, ordinal.score.2,
    alternative = "two.sided", alpha = 0.05
)
