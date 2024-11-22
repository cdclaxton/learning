library(car)

dependent.variable <- c(3083, 3140, 3218, 3239, 3295, 3374, 3475, 3569, 3597, 3725, 3794, 3959, 4043, 4194)
independent.variable <- c(75, 78, 80, 82, 84, 88, 93, 97, 65, 104, 109, 115, 120, 127)

# 9th observation p-value is significant => observation is an outlier
outlierTest(lm(dependent.variable ~ independent.variable))
