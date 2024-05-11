library(circular)

# Angles of the turtles in degrees
turtles[, 2]


# Directions from which 10 green sea turtles approached their nesting island
turtles_radians <- turtles[, 2] * pi / 180

# p-value < 0.05 => reject null hypothesis
# data is not uniformly distributed on the circle
rao.spacing.test(turtles_radians)
