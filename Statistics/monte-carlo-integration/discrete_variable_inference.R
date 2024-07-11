# Inference with discrete variables
# 
#    e <-- theta [Bernoulli random variable]
#    |
#    v
#    h <-- CPT [actual heading]
#    |
#    v
#    h' <-- CPT [measured heading]
#

# Parameters
theta <- 0.8
a <- 0.5
b <- 0.75
c <- 0.9
d <- 0.8

# Build the CPTs
h.cpt <- matrix(c(a, b, 1-a, 1-b), nrow = 2)
rownames(h.cpt) <- c(0, 1)
colnames(h.cpt) <- c("f", "b")

h.prime.cpt <- matrix(c(c, 1-d, 1-c, d), nrow = 2)
rownames(h.prime.cpt) <- c("f", "b")
colnames(h.prime.cpt) <- c("f", "b")

# Estimate the probability p(e|h') using simulation
n.samples <- 10000
df <- data.frame(e = rep(NA,n.samples),
                 h = rep(NA,n.samples),
                 h.prime = rep(NA,n.samples))
for (i in 1:n.samples) {
  e <- rbinom(1, 1, theta)  # Was the observation due to the activity?
  h <- colnames(h.cpt)[which(rmultinom(1, 1, h.cpt[e + 1,]) == 1)]
  h.prime <- colnames(h.prime.cpt)[which(rmultinom(1, 1, h.prime.cpt[h,]) == 1)]
  
  # Store the values in the data frame
  df[i,]$e = e
  df[i,]$h = h
  df[i,]$h.prime = h.prime
}

cond.prob <- function(df, e, h.prime) {
  # Calculate the conditional probability.
  # 
  
  # Calculate p(e, h')
  n1 <- df[df$e == e & df$h.prime == h.prime, ]
  p1 <- nrow(n1) / nrow(df)
  
  # Calculate p(h')
  n2 <- df[df$h.prime == h.prime, ]
  p2 <- nrow(n2) / nrow(df)
  
  # Calculate p(e | h') = p(e, h') / p(h')
  p1 / p2
}

# Calculate the theoretical values
p1 <- theta*((1-b)*(1-d) + b*c) / 
  (theta*(b*c + (1-b)*(1-d)) + (1-theta)*(a*c + (1-a)*(1-d)))

p2 <- theta*(b*(1-c) + (1-b)*d) /
  (theta*(b*(1-c) + (1-b)*d) + (1-theta)*(a*(1-c) + d*(1-a)))

p3 <- 1 - p1
p4 <- 1 - p2

# Display the estimated probabilities and the calculated values
cat("p(e=1 | h'=f) = ", cond.prob(df, 1, "f"), "[", p1, "]\n")
cat("p(e=1 | h'=b) = ", cond.prob(df, 1, "b"), "[", p2, "]\n")
cat("p(e=0 | h'=f) = ", cond.prob(df, 0, "f"), "[", p3, "]\n")
cat("p(e=0 | h'=b) = ", cond.prob(df, 0, "b"), "[", p4, "]\n")
