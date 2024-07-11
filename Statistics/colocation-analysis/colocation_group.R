# Functions to support the generation of colocation groups.

calc.centroid <- function(lats, longs, indices) {
  # Calculate the centroid of the points given their indices.
  #
  # Args:
  #   lats: Vector of latitudes.
  #   longs: Vector of longitudes.
  #   indices: Vector of indices.
  #
  # Returns:
  #   Vector of (lat, long) of the centroid.
  
  # Preconditions
  stopifnot(is.vector(lats))
  stopifnot(is.vector(longs))
  stopifnot(is.vector(indices))
  stopifnot(length(lats) == length(longs))
  stopifnot(length(lats) > 0)
  
  # Calculate the centroid
  centroid.lat <- sum(lats[indices]) / length(indices)
  centroid.long <- sum(longs[indices]) / length(indices)
  
  # Return the centroid
  return(c(centroid.lat, centroid.long))
}

calc.colocation.groups <- function(C) {
  # Calculate the co-location groups.
  #
  # Args:
  #   C: Co-location matrix.
  #
  # Returns:
  #   List of lists.
  
  # Preconditions
  stopifnot(is.matrix(C))
  stopifnot(dim(C)[1] == dim(C)[2])  # matrix must be square
  
  # Create an empty list of co-located nodes
  v <- list()
  
  # Walk through each column in the colocation matrix
  for (i in 1:ncol(C)) {
    matching.indices <- which(C[,i] == TRUE)  # which nodes are co-located?
    if (length(matching.indices) > 0) {
      v <- c(v, list(c(i, matching.indices)))
    }
  }
  
  # Postconditions
  
  # Return the colocation groups
  return(v)
}

calc.colocation.groups.centroids <- function(lats, longs, groups) {
  # Calculate the centroids of the colocation groups.
  #
  # Args:
  #   lats: Vector of latitudes.
  #   longs: Vector of longitudes.
  #   groups: List of groups.
  #
  # Returns:
  #   Dataframe of centroids (columns named 'lat' and 'long')
  
  # Preconditions
  stopifnot(is.vector(lats))
  stopifnot(is.vector(longs))
  stopifnot(length(lats) == length(longs))
  stopifnot(length(lats) > 0)
  all.indices <- unlist(groups)
  stopifnot(min(all.indices) > 0)
  stopifnot(max(all.indices) <= length(lats))
  
  # Create a dataframe to hold the centroids
  N <- length(groups)
  df <- data.frame(lat = rep(NA,N), 
                   long = rep(NA, N))
  
  # Walk through each group
  for (i in 1:N) {
    indices <- groups[[i]]  # get the indices of the nodes in the group
    centroid <- calc.centroid(lats, longs, indices)  # calculate the centroid of the group
    df[i,]$lat <- centroid[1]
    df[i,]$long <- centroid[2]
  }
  
  # Postcondition
  stopifnot(!any(is.na(df)))
  
  # Return the dataframe of centroids
  return(df)
}
