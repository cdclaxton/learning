library(lmtest)

dependent.variable <- c(3083, 3140, 3218, 3239, 3295, 3374, 3475, 3569, 3597, 3725, 3794, 3959, 4043, 4194)
independent.variable <- c(75, 78, 80, 82, 84, 88, 93, 97, 99, 104, 109, 115, 120, 127)

# Fit a linear model
lm.model <- lm(independent.variable ~ dependent.variable)
lm.model

# p-value = 0.04 < 0.05 => reject null hypothesis that errors are uncorrelated
bgtest(lm.model, order = 1)

# p-value = 0.277 > 0.05 => accept the null hypothesis that errors are uncorrelated
bgtest(lm.model, order = 4)
