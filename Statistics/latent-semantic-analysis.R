# Latent semantic analysis

A = matrix(c(1,2,3,4,5,6), nrow=3)

# Perform SVD
r = svd(A)

# Reconstruct matrix A
U = r$u
S = diag(r$d)
V = r$v

A2 = U %*% S %*% V

# ------------------------------------------------------------------------------
# Example from:
# http://webhome.cs.uvic.ca/~thomo/svd.pdf
# ------------------------------------------------------------------------------

# Documents:
# d1 : Romeo and Juliet.
# d2 : Juliet: O happy dagger!
# d3 : Romeo died by dagger.
# d4 : "Live free or die", that's the New-Hampshire's motto.
# d5 : Did you know, New-Hampshire is in New-England.

A = matrix(c(1,0,1,0,0, 
             1,1,0,0,0,
             0,1,0,0,0,
             0,1,1,0,0,
             0,0,0,1,0,
             0,0,1,1,0,
             0,0,0,1,0,
             0,0,0,1,1),
           nrow=5)

A = t(A)  # Transpose the matrix

terms <- c('romeo', 'juliet', 'happy', 'dagger', 'live', 'die', 'free', 'new-hampshire')
docs <- c('d1', 'd2', 'd3', 'd4', 'd5')

rownames(A) <- terms
colnames(A) <- docs

# Document-document matrix
# B[i,j] = number of words in common in documents i and j
B <- t(A) %*% A

# Term-term matrix
# C[i,j] = number of times terms i and j occur together
C <- A %*% t(A)

# Perform SVD
r <- svd(A)
S <- r$u            # matrix of eigenvectors of B
SIGMA <- diag(r$d)  # matrix of singular values
U_T <- r$v          # matrix of eigenvectors of C

plot(r$d)

# First singular value
d <- rep(0, length(r$d))
d1 <- d
d1[1] <- r$d[1]
X <- S %*% diag(d1) %*% U_T
Y <- X %*% t(X)
rownames(Y) <- terms
colnames(Y) <- terms

library(lattice)
levelplot(Y)


# Keep only the first two singular values
S2 <- S[,1:2]
SIGMA2 <- SIGMA[1:2, 1:2]
U_T2 <- U_T[,1:2]

terms_cs <- S2 %*% SIGMA2  # terms in concept space





