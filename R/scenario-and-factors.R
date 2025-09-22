# 
# Probabilities s = [ p(s_0), p(s_1), ..., p(s_{N-1}) ]
# CPTs p(f|c) = [ p(f_0|c), p(f_1|c), ..., p(f_{M-1}|c) ]
# CPT p(f_j|c) = [ p(f_j=1|c=0), p(f_j=1|c=1) ]
# CPT p(c=1|s)

library(rjags)

# ------------------------------------------------------------------------------
# Closed form solution
# ------------------------------------------------------------------------------

valid_probability <- function(p) {
    valid <- (0.0 <= p && p <= 1.0)
    if (valid == FALSE) {
        cat("Probability is not valid:", p)
    }
    return(valid)
}

# Build an OR gate CPT for p(c=1|s) with N inputs
build_or_gate_cpt <- function(N) {
    stopifnot(N > 0)

    cpt <- rep(1, 2^N)
    cpt[1] = 0
    return(cpt)
}

# Build the CPT p(f_j=1|c)
build_p_f_given_c <- function(p_f_given_not_c, p_f_given_c) {
    stopifnot(valid_probability(p_f_given_c))
    stopifnot(valid_probability(p_f_given_not_c))

    return(c(p_f_given_not_c, p_f_given_c))
}

prod_p_f_given_c <- function(c, f, cpt_f) {
    stopifnot(c == 0 || c == 1)
    stopifnot(length(f) == nrow(cpt_f))
    stopifnot(ncol(cpt_f) == 2)

    M <- length(f)
    p = 0.0
    for (j in 1:M) {
        idx <- f[j] + 1

        if (c == 0) {
            p = p + log(1- cpt_f[j, idx])
        } else {
            p = p + log(cpt_f[j, idx])
        }
    }

    p = exp(p)
    stopifnot(valid_probability(p))

    return(p)
}

prod_s <- function(s, p_si) {
    stopifnot(length(s) == length(p_si))

    N <- length(s)
    p = 0.0
    for (i in 1:N) {
        if (s[i] == 1) {
            p = p + log(p_si[i])
        } else {
            p = p + log(1 - p_si[i])
        }
    }

    p = exp(p)
    stopifnot(valid_probability(p))

    return(p)
}

# Row index in a CPT p(c|s)
row_index <- function(s) {
    total = 0
    N <- length(s)
    for (i in 1:N) {
        total = total + s[i] * 2^(N-i)
    }

    return(total+1)
}

sum_product_term <- function(c, p_si, p_c_given_s) {
    stopifnot(c == 0 || c == 1)
    stopifnot(length(p_si) > 0)
    
    # Create a table of the different states of s
    N <- length(p_si)
    l <- rep(list(0:1), N)
    grid <- expand.grid(l)

    total = 0.0
    for (i in 1:nrow(grid)) {
        s <- array(unlist(grid[i,]))
        r <- row_index(s)
        stopifnot(1 <= r && r <= length(p_c_given_s))

        p <- p_c_given_s[r]
        stopifnot(valid_probability(p))

        if (c == 1) {
            total = total + prod_s(s, p_si) * p
        } else {
            total = total + prod_s(s, p_si) * (1 - p)
        }
    }

    return(total)
}

p_c_given_f <- function(c, p_si, p_c_given_s, f, cpts_f) {
    num <- prod_p_f_given_c(c, f, cpts_f) * sum_product_term(c, p_si, p_c_given_s)
    den <- prod_p_f_given_c(0, f, cpts_f) * sum_product_term(0, p_si, p_c_given_s) + 
        prod_p_f_given_c(1, f, cpts_f) * sum_product_term(1, p_si, p_c_given_s)
    return(num/den)
}

p_si <- c(0.7, 0.8)

p_c_given_s <- build_or_gate_cpt(length(p_si))
p_c_given_s <- c(0.1, 0.2, 0.6, 0.9)

f <- c(0, 0, 1)

cpt_f0 <- build_p_f_given_c(0.2, 0.9)
cpt_f1 <- build_p_f_given_c(0.5, 0.5)
cpt_f2 <- build_p_f_given_c(0.1, 0.7)
cpts_f <- matrix(c(cpt_f0, cpt_f1, cpt_f2), nrow=3, byrow=TRUE)

# Calculate p(c=1|f) using the closed form solution
p_closed_form <- p_c_given_f(1, p_si, p_c_given_s, f, cpts_f)

# ------------------------------------------------------------------------------
# JAGS model
# ------------------------------------------------------------------------------

model_string <- "
model {
    for (i in 1:N) {
        s_prime[i] ~ dbern(p_s[i])
    }

    # Calculate the index in the CPT for p(c=1|s_prime)
    for (i in 1:N) {
        k[i] = s_prime[i] * 2^(N-i)
    }
    idx <- round(sum(k) + 1)

    # Probability of the scenario occurring
    p_c <- p_c_given_s[idx]

    # Scenario
    c ~ dbern(p_c)

    # M factors
    for (j in 1:M) {
        f[j] ~ dbern(cpts_f[j, c+1])
    }
}
"

model <- jags.model(textConnection(model_string),
    data = list(
        p_s = p_si,
        N = length(p_si),
        p_c_given_s = p_c_given_s,
        cpts_f = cpts_f,
        f = f,
        M = length(f)
        )
    )

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("c", "idx", "s_prime"),
    n.iter = 20000,
    progress.bar = "none")

# plot(samples)

mat <- as.matrix(samples)

# ------------------------------------------------------------------------------
# Display results
# ------------------------------------------------------------------------------

cat("Closed form: p(c|f) =", p_closed_form, "\n")
cat("Mean of c:", mean(mat[, "c"]), "\n")

# ------------------------------------------------------------------------------
# Closed form solution of model with soft evidence (Pearl's approach)
# ------------------------------------------------------------------------------

log_p_fi_given_c <- function(f, c, cpt_f) {
    stopifnot(f == 0 || f == 1)
    stopifnot(c == 0 || c == 1)

    # p(f=1|c)
    p <- cpt_f[c+1]

    if (f == 1) {
        return(log(p))
    }
    return(log(1-p))
}

log_p_gi_given_fi <- function(g, f, cpt_g) {
    stopifnot(f == 0 || f == 1)
    stopifnot(g == 0 || g == 1)

    # p(g=1|f)
    p <- cpt_g[f+1]

    if (g == 1) {
        return(log(p))
    }
    return(log(1-p))    
}

log_joint <- function(s, c, f, g, p_si, p_c_given_s, cpts_f, cpts_g) {
    stopifnot(length(s) > 0)
    stopifnot(c == 0 || c == 1)
    stopifnot(length(f) == length(g))
    stopifnot(length(s) == length(p_si))
    stopifnot(nrow(p_c_given_s) == 2^length(p_si))
    stopifnot(nrow(cpts_f) == length(f))
    stopifnot(nrow(cpts_g) == length(g))

    # Calculate \sum_{i=0}^{N-1} ln p(s_i)
    N <- length(s)
    term_1 <- 0.0
    for (i in 1:N) {
        if (s[i] == 0) {
            term_1 = term_1 + log(1 - p_si[i])
        } else {
            term_1 = term_1 + log(p_si[i])
        }
    }

    # Calculate ln p(c|s)
    idx <- row_index(s)
    if (c == 0) {
        term_2 <- log(1 - p_c_given_s[idx])
    } else {
        term_2 <- log(p_c_given_s[idx])
    }

    # Calculate \sum_{j=0}^{M-1} ( ln p(f_i|c) + ln(g_i|f_i) )
    term_3 <- 0.0
    for (j in 1:M) {
        term_3 = term_3 + log_p_fi_given_c(f[j], c, cpts_f[j,]) + log_p_gi_given_fi(g[j], f[j], cpts_g[j,])
    }

    return(term_1 + term_2 + term_3)
}

# Calculate p(c,g)
p_c_g <- function(p_s, c, g, p_c_given_s, cpts_f, cpts_g) {

    N <- length(p_s)
    l <- rep(list(0:1), N)
    grid_s <- expand.grid(l)

    M <- length(g)
    l2 <- rep(list(0:1), M)
    grid_f <- expand.grid(l2)    

    total <- 0.0
    for (i in 1:nrow(grid_s)) {
        s <- array(unlist(grid_s[i,]))

        for (j in 1:nrow(grid_f)) {
            f <- array(unlist(grid_f[j,]))

            total = total + exp(log_joint(s, c, f, g, p_s, p_c_given_s, cpts_f, cpts_g))
        }
    }

    stopifnot(valid_probability(total))
    return(total)
}

# Calculate p(c=1|g=[1,1,..,1])
p_c_given_g <- function(M, p_si, p_c_given_s, cpts_f, cpts_g) {
    g <- rep(1, M)
    p1 <- p_c_g(p_si, 1, g, p_c_given_s, cpts_f, cpts_g)
    p2 <- p_c_g(p_si, 0, g, p_c_given_s, cpts_f, cpts_g)

    return(p1/(p1+p2))
}

# Build the CPT p(g_j=1|f)
build_p_g_given_f <- function(p_g_given_not_f, p_g_given_f) {
    stopifnot(valid_probability(p_g_given_f))
    stopifnot(valid_probability(p_g_given_not_f))

    return(c(p_g_given_not_f, p_g_given_f))
}

p_si <- c(0.1, 0.2)

p_c_given_s <- build_or_gate_cpt(length(p_si))
p_c_given_s <- c(0.1, 0.2, 0.6, 0.9)

cpt_f0 <- build_p_f_given_c(0.9, 0.2)
cpt_f1 <- build_p_f_given_c(0.5, 0.5)
cpt_f2 <- build_p_f_given_c(0.1, 0.7)
cpts_f <- matrix(c(cpt_f0, cpt_f1, cpt_f2), nrow=3, byrow=TRUE)

p_f <- c(0.7, 0.2, 0.8)
cpt_g0 <- build_p_g_given_f(1-p_f[1], p_f[1])
cpt_g1 <- build_p_g_given_f(1-p_f[2], p_f[2])
cpt_g2 <- build_p_g_given_f(1-p_f[3], p_f[3])
cpts_g <- matrix(c(cpt_g0, cpt_g1, cpt_g2), nrow=3, byrow=TRUE)

M <- length(p_f)
posterior <- p_c_given_g(M, p_si, p_c_given_s, cpts_f, cpts_g)

# ------------------------------------------------------------------------------
# JAGS model with soft evidence
# ------------------------------------------------------------------------------

model_string <- "
model {
    for (i in 1:N) {
        s_prime[i] ~ dbern(p_s[i])
    }

    # Calculate the index in the CPT for p(c=1|s_prime)
    for (i in 1:N) {
        k[i] = s_prime[i] * 2^(N-i)
    }
    idx <- round(sum(k) + 1)

    # Probability of the scenario occurring
    p_c <- p_c_given_s[idx]

    # Scenario
    c ~ dbern(p_c)

    # M factors
    for (j in 1:M) {
        f[j] ~ dbern(cpts_f[j, c+1])
    }

    # Soft evidence for the factors
    for (j in 1:M) {
        g[j] ~ dbern(cpts_g[j, f[j]+1])
    }
}
"

model <- jags.model(textConnection(model_string),
    data = list(
        p_s = p_si,
        N = length(p_si),
        p_c_given_s = p_c_given_s,
        cpts_f = cpts_f,
        cpts_g = cpts_g,
        M = length(p_f),
        g = rep(1, M)
    )
)

update(model, n.iter = 100000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("c"),
    n.iter = 10000,
    progress.bar = "none")

# plot(samples)

mat <- as.matrix(samples)

cat("Posterior of closed form solution with soft evidence = ", posterior, "\n")
cat("Mean of c:", mean(mat[, "c"]), "\n")

# ------------------------------------------------------------------------------
# Closed form solution of model with soft evidence (Jeffrey's approach)
# ------------------------------------------------------------------------------

# ln p(s,c,f)
#
# s = vector of states of s, e.g. c(0,1,1)
# c = state of the scenario (0 or 1)
# f = observed state of the factors, e.g c(1,0)
# p_s = prior probability of each situation
# p_c_given_s = p(c|s)
# cpts_f = p(f|c)
ln_p_s_c_f <- function(s, c, f, p_s, p_c_given_s, cpts_f) {

    stopifnot(length(s) > 0)
    stopifnot(c == 0 || c == 1)
    stopifnot(length(s) == length(p_s))
    stopifnot(nrow(p_c_given_s) == 2^length(p_s))
    stopifnot(nrow(cpts_f) == length(f))

    # Calculate \sum_{i=0}^{N-1} ln p(s_i)
    N <- length(s)
    term_1 <- 0.0
    for (i in 1:N) {
        if (s[i] == 0) {
            term_1 = term_1 + log(1 - p_s[i])
        } else {
            term_1 = term_1 + log(p_s[i])
        }
    }

    # Calculate ln p(c|s)
    idx <- row_index(s)
    if (c == 0) {
        term_2 <- log(1 - p_c_given_s[idx])
    } else {
        term_2 <- log(p_c_given_s[idx])
    }

    # Calculate \sum_{j=0}^{M-1} ln p(f_i|c)
    term_3 <- 0.0
    for (j in 1:M) {
        term_3 = term_3 + log_p_fi_given_c(f[j], c, cpts_f[j,])
    }

    ln_p <- term_1 + term_2 + term_3

    stopifnot(valid_probability(exp(ln_p)))
    return(ln_p)
}

p_c_and_f <- function(c, f, p_s, p_c_given_s, cpts_f) {
    stopifnot(c == 0 || c == 1)
    stopifnot(length(p_s) > 0)
    
    # Create a table of the different states of s
    N <- length(p_s)
    l <- rep(list(0:1), N)
    grid <- expand.grid(l)

    total = 0.0
    for (i in 1:nrow(grid)) {
        s <- array(unlist(grid[i,]))
        r <- row_index(s)
        stopifnot(1 <= r && r <= length(p_c_given_s))

        total = total + exp(ln_p_s_c_f(s, c, f, p_s, p_c_given_s, cpts_f))
    }

    stopifnot(valid_probability(total))
    return(total)
}

# p(c=1|f)
p_c_given_f2 <- function(f, p_s, p_c_given_s, cpts_f) {
    num <- p_c_and_f(1, f, p_s, p_c_given_s, cpts_f)
    den <- p_c_and_f(0, f, p_s, p_c_given_s, cpts_f) + p_c_and_f(1, f, p_s, p_c_given_s, cpts_f)

    p <- num/den
    stopifnot(valid_probability(p))

    return(p)
}

calc_weight <- function(f, p_f) {
    stopifnot(length(f) == length(p_f))

    M <- length(p_f)
    p <- rep(0, M)
    for (j in 1:M) {
        if (f[j] == 0) {
            p[j] = 1 - p_f[j]
        } else {
            p[j] = p_f[j]
        }
    }

    weight <- exp(sum(log(p)))
    stopifnot(valid_probability(weight))

    return(weight)
}

# Posterior using Jeffrey's approach to combining uncertain observations
calc_posterior2 <- function(c, p_s, p_c_given_s, cpts_f, p_f) {
    
    # Create a table of the different states of f
    M <- length(p_f)
    l <- rep(list(0:1), M)
    grid <- expand.grid(l)

    total = 0.0
    for (i in 1:nrow(grid)) {
        f <- array(unlist(grid[i,]))

        total = total + calc_weight(f, p_f) * p_c_given_f2(f, p_s, p_c_given_s, cpts_f) 
    }

    stopifnot(valid_probability(total))
    return(total)
}

posterior2 <- calc_posterior2(1, p_si, p_c_given_s, cpts_f, p_f)
cat("Posterior of closed form solution with soft evidence using Jeffrey's approach = ", posterior2, "\n")