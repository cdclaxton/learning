# Noisy OR probability calculation

p <- function(x1, p1, x2, p2, leak) {
  # Calculate the probability of the output node using a noisy OR.
  #
  # Args:
  #   x1: State of input node 1 (1 or 0).
  #   p1: Probability 1.
  #   x2: State of input node 2 (1 or 0).
  #   p1: Probability 2.
  #   leak: Leak probability (= prob. of output node when both inputs are 0).
  # 
  # Returns:
  #   Probability of the output node.
  
  1 - (1 - leak)*((1 - p1)^x1 * (1-p2)^x2)
}

p1 <- 0.7
p2 <- 0.9
leak <- 0.01

p(0, p1, 0, p2, leak)  # 0.01 (leak probability)
p(0, p1, 1, p2, leak)  # 1 - (1-leak)*(1-p2)
p(1, p1, 0, p2, leak)  # 1 - (1-leak)*(1-p1)
p(1, p1, 1, p2, leak)  # 1 - (1-leak)*(1-p1)*(1-p2)
