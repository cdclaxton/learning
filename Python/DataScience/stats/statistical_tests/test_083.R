dep <- c(3083, 3140, 3218, 3239, 3295, 3374, 3475, 3569, 3597, 3725, 3794, 3959, 4043, 4194)
ind.1 <- c(75, 78, 80, 82, 84, 88, 93, 97, 99, 104, 109, 115, 120, 127)
ind.2 <- c(5, 8, 0, 2, 4, 8, 3, 7, 9, 10, 10, 15, 12, 12)

model <- lm(dep ~ ind.1 + ind.2)

# Test whether 2nd or 3rd powers of the independent variables should
# be included
# p-value = 0.2626 > 0.05 => don't reject null hypothesis of linearity
lmtest::resettest(model, power = 2:3, type = "regressor")
