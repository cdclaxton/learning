library(circular)

# Directions from which 10 green sea turtles approached their nesting island
turtles_radians <- turtles[, 2] * pi / 180

# p-value < 0.05 => reject null hypothesis (therefore data is not
# uniformly distributed on circle)
kuiper.test(turtles_radians)
