# Monte Carlo integration -- area of a circle
# Circle has a unit radius (therefore the diameter = 2)
#
# Area of square = 2 * 2 = 4
# Proportion of points within circle = area of circle / area of square
# Therefore, area of circle = Proportion of points within circle * area of square
# a = p * 4

library(ggplot2)

# Parameters
n.samples <- 1000  # number of samples to generate
expected.area <- pi  # pi * r^2 where r = 1

df <- data.frame(n = 1:n.samples, within = rep(NA, n.samples))

for (i in 1:n.samples) {
  
  # Generate a random point in a 
  p <- runif(2, -1, 1)
  x <- p[1]
  y <- p[2]
  
  # Is the point within the circle?
  df[i,]$within <- (x^2 + y^2 <= 1) * 1
}

df$cumsum <- cumsum(df$within)
df$area <- apply(df, 1, function(r) 4*r['cumsum'] / r['n'])

ggplot(df, mapping = aes(x = n, y = area)) + 
  geom_line(col = "blue") +
  geom_hline(yintercept = pi, col = "red") +
  xlab("Number of samples") + ylab("Estimate of pi")