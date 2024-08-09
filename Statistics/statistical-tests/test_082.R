dependent.variable <- c(3083, 3140, 3218, 3239, 3295, 3374, 3475, 3569, 3597, 3725, 3794, 3959, 4043, 4194)
independent.variable <- c(75, 78, 80, 82, 84, 88, 93, 97, 99, 104, 109, 115, 120, 127)

# p-value = 0.3169 > 0.05 => don't reject the null hypothesis of linearity
lmtest::harvtest(lm(dependent.variable ~ independent.variable))
