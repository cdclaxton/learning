# Inference on a Bayesian network using Monte Carlo integration.
#
#   e <-- theta  [Bernoulli] Event occurred?
#   |
#   V
#   x [Sample from a polygon]
#   |
#   V
#   x' <-- [Gaussian] Measurement noise
#

library(mgcv)

gen.sample.in.polygon <- function(coords) {
  # Generate a sample from within a polygon
  #
  # Args:
  #   coords: Nx2 matrix of x,y coordinates
  #
  # Returns:
  #   1x2 matrix containing a point within the polygon
  
  # Get the axis-aligned bounding box of the polygon
  xmin <- min(coords[,1], na.rm = TRUE)
  xmax <- max(coords[,1], na.rm = TRUE)
  ymin <- min(coords[,2], na.rm = TRUE)
  ymax <- max(coords[,2], na.rm = TRUE)
  
  # Generate random points until a point within the polygon is found
  inside <- FALSE
  while (!inside) {
    x <- runif(1, xmin, xmax)
    y <- runif(1, ymin, ymax)
    pt <- matrix(c(x,y), nrow = 1)
    inside <- in.out(coords, pt)
  }
  
  # Return the coordinate
  matrix(c(x,y), nrow = 1)
}

gen.N.samples.in.polygon <- function(N, coords) {
  # Generate N samples that fall within a polygon.
  # 
  # Args:
  #   n: Number of samples to generate.
  #   coords: Coordinates of the polygon.
  #
  # Returns:
  #   Nx2 matrix of samples.
  
  m <- matrix(rep(NA,2*N), nrow = N)
  for (i in 1:N) {
    m[i,] <- gen.sample.in.polygon(coords)
  }
  return(m)
}

# Get a polygon
data(columb.polys)
bnd <- columb.polys[[2]]

# Plot the polygon
plot(bnd, type="n", xlim=c(7,9), ylim = c(12,15), xlab = "x", ylab = "y")
polygon(bnd)
pt <- gen.N.samples.in.polygon(100, bnd)
lines(pt, col = "red", type = "p")
