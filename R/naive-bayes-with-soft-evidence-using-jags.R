# Naive Bayes model with soft evidence using JAGS

library(rjags)

# JAGS model
model_string <- "
model {
    # Class
    c ~ dbern(p_c)

    # Factor
    f0 ~ dbern(cpt_f0[c + 1, 2])
    f1 ~ dbern(cpt_f1[c + 1, 2])

    # Soft evidence for a factor
    g0 ~ dbern(cpt_g0[f0 + 1, 2])
    g1 ~ dbern(cpt_g1[f1 + 1, 2])
}
"

# Prior probability of the class c
p_c <- 0.6

# CPTs p(f_i | c)
#
#         f_i
#      | 0  1
#  ------------
#    0 | a  b
#  c 1 | c  d
#
p_f0_given_c_0 = 0.5
p_f0_given_c_1 = 0.8

p_f1_given_c_0 = 0.3
p_f1_given_c_1 = 0.6

cpt_f0 <- matrix(c(
    (1-p_f0_given_c_0), p_f0_given_c_0,
    (1-p_f0_given_c_1), p_f0_given_c_1
    ), nrow = 2, byrow = TRUE)

cpt_f1 <- matrix(c(
    (1-p_f1_given_c_0), p_f1_given_c_0,
    (1-p_f1_given_c_1), p_f1_given_c_1
    ), nrow = 2, byrow = TRUE)

# Soft evidence for the factors
p_f0 <- 0.7
p_f1 <- 0.8

# CPTs for the soft evidence p(g_i | f_i)
#
#            g
#      |  0    1
#  ---------------
#    0 |  r   1-r
#  f 1 | 1-r   r
#
cpt_g0 <- matrix(c(
    p_f0,   1-p_f0,
    1-p_f0, p_f0
    ), nrow = 2, byrow = TRUE)

cpt_g1 <- matrix(c(
    p_f1,   1-p_f1,
    1-p_f1, p_f1
    ), nrow = 2, byrow = TRUE)

# Calculate the product term given by:
#
# \prod_{i=0}^{M-1} p(f_i | c) p(g_i | f_i)
product_term <- function(c, f, g, cpts_f, cpts_g) {
    stopifnot(0 <= c && c <= 1)
    stopifnot(length(f) == length(g))
    stopifnot(length(cpts_f) == length(f))
    stopifnot(length(cpts_g) == length(g))

    # Number of factors
    M <- length(f)
    p <- 1

    for (i in 1:M) {
        fi <- f[i]
        stopifnot(0 <= fi && fi <= 1)

        gi <- g[i]
        stopifnot(0 <= gi && gi <= 1)

        cpt_f <- cpts_f[[i]]
        cpt_g <- cpts_g[[i]]

        p = p * cpt_f[c+1, fi+1] * cpt_g[fi+1, gi+1]
    }

    return(p)
}

# Calculate the sum term given by:
#
# \sum_{f} \product_{i=0}^{M-1} p(f_i | c) p(g_i | f_i)
sum_term <- function(c, M, g, cpts_f, cpts_g) {

    # Create a table of the different states of f
    l <- rep(list(0:1), M)
    grid <- expand.grid(l)
    
    total <- 0.0
    for (i in 1:nrow(grid)) {
        f <- array(unlist(grid[i,]))
        total = total + product_term(c, f, g, cpts_f, cpts_g)
    }

    return(total)
}

# Calculate the expected posterior probability of the class
g <- c(1, 1)
cpts_f <- list(cpt_f0, cpt_f1)
cpts_g <- list(cpt_g0, cpt_g1)

num <- p_c * sum_term(1, 2, g, cpts_f, cpts_g)
den <-  p_c * sum_term(1, 2, g, cpts_f, cpts_g) + (1 - p_c) * sum_term(0, 2, g, cpts_f, cpts_g)
posterior <- num / den

model <- jags.model(textConnection(model_string),
    data = list(
        cpt_f0 = cpt_f0, 
        cpt_f1 = cpt_f1, 
        p_c = p_c,
        cpt_g0 = cpt_g0,
        cpt_g1 = cpt_g1,
        g0 = 1, 
        g1 = 1)
    )

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("c"),
    n.iter = 20000,
    progress.bar = "none")

# plot(samples)

mat <- as.matrix(samples)
cat("Mean of c:", mean(mat[, "c"]), "\n")
cat("Posterior probability p(c=1|g) =", posterior, "\n")