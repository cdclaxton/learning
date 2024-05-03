library(car)

dependent.variable <- c(3083, 3140, 3218, 3239, 3295, 3374, 3475, 3569, 3597, 3725, 3794, 3959, 4043, 4194)
independent.variable <- c(75, 78, 80, 82, 84, 88, 93, 97, 99, 104, 109, 115, 120, 127)

# Fit a linear model
lm.model <- lm(independent.variable ~ dependent.variable)
lm.model

par(mfrow = c(2, 1))
plot(dependent.variable, independent.variable, pch = 16, cex = 1.3, col = "blue")
abline(lm.model)

# Plot the residuals
plot(dependent.variable, resid(lm.model),
    pch = 16, cex = 1.3, col = "blue",
    ylab = "Residuals", main = "Residuals"
)
abline(0, 0)

# p-value = 0.08 > 0.05 => don't reject null hypothesis that there is no correlation
# among residuals
durbinWatsonTest(lm.model)

# Test for lags 1, 2, 3
durbinWatsonTest(lm.model, max.lag = 3)
