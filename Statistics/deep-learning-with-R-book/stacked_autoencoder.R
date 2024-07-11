# Stacked Autoencoder
#
# install.packages('SAENET')

# Clear the workspace
rm(list = ls())

library(SAENET)

ab.url <- 'http://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data'
names <- c('sex', 'length', 'diameter', 'height', 'whole.weight', 'shucked.weight', 
           'viscera.weight', 'shell.weight', 'rings')
data <- read.table(ab.url, header = F, sep = ',', col.names = names)

data$sex <- NULL
data$height[data$height == 0] <- NA
data <- na.omit(data)
data1 <- as.matrix(data)

set.seed(2016)
n <- nrow(data)
train <- sample(1:n, 10, FALSE)

fit <- SAENET.train(X.train = data1[train,],
                    n.nodes = c(5, 4, 2),
                    unit.type = "logistic",
                    lambda = 1e-5,
                    beta = 1e-5,
                    rho = 0.07,
                    epsilon = 0.1,
                    max.iterations = 100,
                    optim.method = c("BFGS"),
                    rel.tol = 0.01,
                    rescale.flag = TRUE,
                    rescaling.offset = 0.001)

fit[[3]]$X.output

