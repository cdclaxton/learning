library(circular)

w <- list(rvonmises(300, circular(0), kappa = 10))
x <- list(rvonmises(300, circular(0), kappa = 20)) # larger dispersion
y <- list(rvonmises(300, circular(0), kappa = 10))
z <- list(rvonmises(300, circular(0), kappa = 10))

sample <- c(w, x, y, z)
rao.test(sample)
