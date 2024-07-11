# Autoencoder
# install.packages(c('autoencoder', 'ripa'))

library(autoencoder)
library(ripa)

data(logo)
image(logo)

x.train <- t(logo)

set.seed(2016)
fit <- autoencode(X.train = x.train,
                  X.test = NULL,
                  nl = 3,  # number of layers
                  N.hidden = 60,  # number of hidden nodes
                  unit.type = "logistic",  # activation function
                  lambda = 1e-5,  # weight decay
                  beta = 1e-5,  # weight of the sparsity penalty term
                  rho = 0.3,  # sparsity
                  epsilon = 0.1,  # normal dist.
                  max.iterations = 100,
                  optim.method = c("BFGS"),
                  rel.tol = 0.01,
                  rescale.flag = TRUE,  # re-scale values to lie in the range [0,1]
                  rescaling.offset = 0.001)

attributes(fit)

features <- predict(fit, X.input = x.train, hidden.output = TRUE)
image(t(features$X.output))

pred <- predict(fit, X.input = x.train, hidden.output = FALSE)
pred$mean.error

par(mfrow = c(2,2))
image(t(pred$X.output))
image(t(x.train))
image(t(pred$X.output) - t(x.train))

