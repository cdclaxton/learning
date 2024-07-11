# Graph change detection -- unweighted graph
#
# 1. Construct a random graph (with spare, unconnected nodes).
# 2. At each time step randomly select edges to add/remove.
#
# Fit a model to the distribution of the graph distances.
# Build a model that can detect anomalous changes.
# ==============================================================================

library(GGally)
library(stringr)

# ------------------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------------------

num.nodes <- 10
p.start <- 0.2

p.add.normal <- 0.05
p.remove.normal <- 0.05

num.time.steps <- 20
output.folder <- "C:/Users/cdc/OneDrive/Technical/Learning/R/Networks/plots/"

# ------------------------------------------------------------------------------
# Functions 
# ------------------------------------------------------------------------------

make.symmetric <- function(adj) {
  # Make a matrix symmetric (uses the upper-triangular matrix).
  #
  # Args:
  #   adj: Matrix.
  #
  # Returns:
  #   Symmetric matrix.
  
  adj[lower.tri(adj)] = t(adj)[lower.tri(adj)]
  return(adj)
}

build.random.graph <- function(num.nodes, p) {
  # Construct a random graph.
  #
  # Args:
  #   num.nodes: Number of nodes in the graph.
  #   p: Probability of a node i being connected to node j.
  #
  # Returns:
  #   (Symmetric) Adjacency matrix.
  
  # Preconditions
  stopifnot(num.nodes > 0)
  stopifnot(0 < p && p <= 1)
  
  # Build the (empty) random adjacency matrix
  adj <- matrix(0, nrow=num.nodes, ncol=num.nodes)
  
  # Make the upper-triangular adjacency matrix
  for (i in 1:(num.nodes-1)) {
    adj[i, (i+1):num.nodes] <- rbinom(n=(num.nodes-i), size=1, prob=p)
  }
  
  # Make the adjacency matrix symmetric from the upper-triangular version
  adj <- make.symmetric(adj)
  
  # Return the adjacency matrix
  return(adj)
}

perturb.graph <- function(adj, p.add, p.remove) {
  # Perturb the graph (randomly add or remove edges).
  #
  # Args:
  #   adj: Adjacency matrix.
  #   p.add: Probability that an edge is added between two nodes.
  #   p.remove: Probability that an edge is removed between two nodes.
  #
  # Returns:
  #   Perturbed (symmetric) adjacency matrix.
  
  # Perturb the upper-triangular adjacency matrix
  for (i in 1:(num.nodes-1)) {
    
    # Extract the connections from node i
    edges <- adj[i, (i+1):num.nodes]
    
    # Generate the random additions and removals (ignoring connections)
    additions <- rbinom(n=(num.nodes-i), size=1, prob=p.add)
    removals <- rbinom(n=(num.nodes-i), size=1, prob=p.remove)
  
    # Find the edges that could be subject to additions and removals
    valid.additions <- (edges == 0) * additions
    valid.removals <- (edges == 1) * removals
    
    # Add and remove edges
    new.edges <- edges - valid.removals + valid.additions
    
    adj[i, (i+1):num.nodes] <- new.edges
  }
  
  # Make the matrix symmetric
  adj <- make.symmetric(adj)
  
  # Return the adjacency matrix
  return(adj)
}

graph.edit.distance <- function(G, H) {
  # Calculate the distance between the two graphs G and H.
  #
  # The adjacency matrices are assumed to have values of zero to indicate
  # no edge and a value greater than zero for an edge.
  #
  # Args:
  #   G: Adjacency matrix.
  #   H: Adjacency matrix.
  #
  # Returns:
  #   Graph distance.
  
  # Preconditions
  stopifnot(dim(G)[1] == dim(H)[1])
  stopifnot(dim(G)[2] == dim(H)[2])
  
  # Find the number of edges in graphs G and H
  num.edges.G <- sum(G > 0)
  num.edges.H <- sum(H > 0)
  
  # Find the number of edges in common
  same <- (H == G) * (H > 0)
  num.common <- sum(same)

  # Calculate the distance
  dist <- num.edges.G + num.edges.H - (2 * num.common)
  
  # Return the distance
  return(dist)
}

build.filename <- function(i, max.i, name, folder) {
  # Build a filename with padded zeros.
  #
  # Args:
  #   i: Index.
  #   max.i: Maximum value of the index.
  #   name: Remainder of the filename, e.g. _graph.png.
  #
  # Returns:
  #   String with leading zeros, e.g. 019.
  
  # Preconditions
  stopifnot(i >= 0)
  stopifnot(i <= max.i)
  
  num.digits <- ceiling(log10(max.i)) + 1
  digits <- str_pad(i, num.digits, pad = "0")
  
  return(paste0(folder, digits, name))
}

# ------------------------------------------------------------------------------
# Script
# ------------------------------------------------------------------------------

# Build a random graph
adj <- build.random.graph(num.nodes, p.start)

# Plot
net <- network(adj, directed = FALSE)
x = gplot.layout.fruchtermanreingold(net, NULL)
net %v% "x" = x[, 1]
net %v% "y" = x[, 2]

# Save the graph
filename <- build.filename(0, num.time.steps, "_graph.png", output.folder)
ggnet2(net, mode = c("x", "y"), label = 1:10, color = "steelblue")
ggsave(filename)

# Walk through each time step
dists <- rep(NA, num.time.steps)
for (i in 1:num.time.steps) {
  
  # Peturb the graph
  new.adj <- perturb.graph(adj, p.add = p.add.normal, p.remove = p.remove.normal)   
    
  # Calculate the distance
  dists[i] <- graph.edit.distance(adj, new.adj)
  
  # Save the graph
  net <- network(new.adj, directed = FALSE)
  net %v% "x" = x[, 1]
  net %v% "y" = x[, 2]
  
  filename <- build.filename(i, num.time.steps, "_graph.png", output.folder)
  ggnet2(net, mode = c("x", "y"), label = 1:10, color = "steelblue")
  ggsave(filename)
  
  # New graph becomes the old graph
  adj <- new.adj
}

# Plot the graph edit distances as a function of time
plot(dists, xlab = "Time", ylab = "Distance", 
     main = "Graph edit distance")

