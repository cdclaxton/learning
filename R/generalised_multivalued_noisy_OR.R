# Notes from http://staff.utia.cas.cz/vomlel/Voml_3484.pdf
#
# A multi-valued graded child variable
#
#   X1    X2  ...  Xn
#
#    |    |         |
#    v    v         v
#
#   X1'  X2'       Xn'
#
#    |    |         |
#    |    |--> Y <--|
#    |------->
#
# The probability is given in terms of the cumulative distribution:
#
# p(Y <= y | x) = \prod_{i=1}^{N} p(X_i' <= y | X_i = x_i)
#
#               = \prod_{i=1}^{N} p_{y_i, x}

# Calculate cumulative summations per row
calc_cums <- function(m) {

    n_rows <- dim(m)[1]
    n_cols <- dim(m)[2]

    output <- matrix(0, nrow = n_rows, ncol = n_cols)
    for (i in 1:n_rows) {
        for (j in 1:n_cols) {
            if (j == 1) {
                output[i, j] <- m[i, j]
            } else {
                output[i, j] <- output[i, (j - 1)] + m[i, j]
            }
        }
    }

    return(output)
}

# Undo the cumulative sumations
undo_cums <- function(m) {

    n_rows <- dim(m)[1]
    n_cols <- dim(m)[2]

    output <- matrix(0, nrow = n_rows, ncol = n_cols)
    for (i in 1:n_rows) {
        for (j in 1:n_cols) {
            if (j == 1) {
                output[i, j] <- m[i, j]
            } else {
                output[i, j] <- m[i, j] - m[i, j - 1]
            }
        }
    }

    return(output)
}

a <- matrix(c(0.2, 0.4, 0.4,
              0.4, 0.1, 0.5), nrow = 2, byrow = TRUE)

b <- matrix(c(0.9, 0.1, 0.0,
              0.2, 0.7, 0.1,
              0.0, 0.2, 0.8), nrow = 3, byrow = TRUE)

cum_a <- calc_cums(a)
cum_b <- calc_cums(b)

# The CPT is held in an array with indexing:
# x1, x2, y

m1 <- dim(cum_a)[1]
m2 <- dim(cum_b)[1]
y <- dim(cum_a)[2]

m <- array(0, dim = c(m1, m2, y))

for (x1 in 1:m1) {
    for (x2 in 1:m2) {
        for (yi in 1:y) {
            m[x1, x2, yi] <- cum_a[x1, yi] * cum_b[x2, yi]
        }
    }
}

print(m)