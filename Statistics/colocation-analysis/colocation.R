# Co-location analysis

colocated <- function(lats, longs, times, delta.d, delta.t) {
  # Determine samples that are co-located.
  #
  # Args:
  #   lats: Vector of latitudes.
  #   longs: Vector of longitudes.
  #   times: Vector of times.
  #   delta.d: Distance threshold.
  #   delta.t: Time threshold.
  #
  # Returns:
  #   List of matrices (colocated, near in time, near in space).
  
  # Preconditions
  stopifnot(is.vector(lats))
  stopifnot(is.vector(longs))
  stopifnot(is.vector(times))
  stopifnot(length(lats) > 0)
  stopifnot(length(lats) == length(longs))
  stopifnot(length(longs) == length(times))
  stopifnot(is.atomic(delta.d))
  stopifnot(is.atomic(delta.t))  
  
  # Calculate the lower triangular matrix of thresholded Euclidean distances
  N.space <- calc.near.in.space(lats, longs, delta.d)
  
  # Calculate the lower triangular matrix of thresholded time differences
  N.time <- calc.near.in.time(times, delta.t)
  
  # Determine the colocated 'nodes'
  C <- N.space & N.time
  C <- unname(C)
  
  # Postconditions
  N <- length(lats)
  stopifnot(all(dim(C) == c(N, N)))
  stopifnot(all(dim(N.time) == c(N, N)))
  stopifnot(all(dim(N.space) == c(N, N)))
  
  # Return the list of matrices
  return(list(C = C, 
              N.time = N.time, 
              N.space = N.space))
}

calc.near.in.time <- function(times, delta.t) {
  # Calculate samples that are 'near' in time.
  #
  # Args:
  #   times: Vector of times.
  #   delta.t: Time threshold.
  #
  # Returns:
  #   Lower triangular matrix of points that are near in time.
  
  # Preconditions
  stopifnot(is.vector(times))
  stopifnot(length(times) > 0)
  stopifnot(is.atomic(delta.t))  

  # Calculate the lower triangular matrix of time differences and thresholded times
  M.time <- calc.time.differences(times)
  N.time <- threshold.lower.tri.matrix(M.time, delta.t)
  N.time <- unname(N.time)
  
  # Postconditions
  N <- length(times)
  stopifnot(all(dim(N.time) == c(N, N)))
  
  # Return the LT matrix
  return(N.time)
}

calc.near.in.space <- function(lats, longs, delta.d) {
  # Calculate samples that are 'near' in space.
  #
  # Args:
  #   lats: Vector of latitudes.
  #   longs: Vector of longitudes.
  #   delta.d: Distance threshold.
  #
  # Returns:
  #   Lower triangular matrix of points that are near in space.
  
  # Preconditions
  stopifnot(is.vector(lats))
  stopifnot(is.vector(longs))
  stopifnot(length(lats) > 0)
  stopifnot(length(lats) == length(longs))
  stopifnot(is.atomic(delta.d))
  
  # Calculate the lower triangular matrix of distances and thresholded distances
  M.dist <- calc.geo.distances(lats, longs)
  N.dist <- threshold.lower.tri.matrix(M.dist, delta.d)
  N.dist <- unname(N.dist)
  
  # Postconditions
  N <- length(lats)
  stopifnot(all(dim(N.dist) == c(N, N)))
  
  # Return the LT matrix
  return(N.dist)
}

threshold.lower.tri.matrix <- function(M, threshold) {
  # Threshold a lower triangular matrix.
  #
  # Args:
  #   M: Matrix to threshold.
  #   threshold: Threshold to apply.
  #
  # Returns:
  #   Thresholded lower triangular matrix.
  
  # Preconditions
  stopifnot(dim(M)[1] == dim(M)[2])  # matrix must be square
  stopifnot(is.atomic(threshold))
  
  # Apply the threshold to all elements of the matrix
  M.threshold <- M <= threshold
  
  # Make the thresholded matrix lower triangular again
  M.threshold <- lower.tri(M.threshold) * M.threshold
  
  # Return the matrix
  return(M.threshold)
}

calc.time.differences <- function(times) {
  # Calculate the pair-wise time differences between samples.
  #
  # Args:
  #   times: Vector of times.
  # 
  # Returns:
  #   Lower triangular matrix of time differences.
  
  # Precondition
  stopifnot(is.vector(times))
  N <- length(times)
  stopifnot(N > 0)
  
  # Calculate the time differences
  M.time <- as.matrix(dist(times))
  
  # Make the matrix of time differences lower triangular
  M.time <- lower.tri(M.time) * M.time
  
  # Remove the row and column names
  M.time <- unname(M.time)
  
  # Postconditon
  stopifnot(all(dim(M.time) == c(N, N)))
  
  # Return the matrix of time differences
  return(M.time)
}

calc.geo.distances <- function(lats, longs) {
  # Calculate the Euclidean distance between samples.
  #
  # Args:
  #   lats: Vector of latitudes.
  #   longs: Vector of longitudes.
  #
  # Returns:
  #   Lower triangular matrix of distances.
  
  # Preconditions
  stopifnot(is.vector(lats))
  stopifnot(is.vector(longs))
  stopifnot(length(lats) > 0)
  stopifnot(length(lats) == length(longs))
  
  # Compute the pairwise distances for the latitudes and longitudes
  M.delta.lats <- as.matrix(dist(lats))
  M.delta.longs <-as.matrix(dist(longs))
  
  # Make the pairwise distances lower triangular
  M.delta.lats <- lower.tri(M.delta.lats) * M.delta.lats
  M.delta.longs <- lower.tri(M.delta.longs) * M.delta.longs
  
  # Compute the Euclidean distance
  M.dist <- (M.delta.lats^2 + M.delta.longs^2) ^ 0.5
  
  # Remove the row and column names
  M.dist <- unname(M.dist)
  
  # Postcondition
  N <- length(lats)
  stopifnot(all(dim(M.dist) == c(N, N)))
  
  # Return the matrix
  return(M.dist)
}
