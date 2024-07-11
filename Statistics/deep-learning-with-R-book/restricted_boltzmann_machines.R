# Restricted Boltzmann Machines
#
# install.packages('RcppDL')
# install.packages('ltm')

# Clear the workspace
rm(list = ls())

library(RcppDL)
library(ltm)

data(Mobility)
data <- Mobility

set.seed(2395)
n <- nrow(data)
sample <- sample(1:n, 1000, FALSE)
data <- as.matrix(Mobility[sample,])

n <- nrow(data)
train <- sample(1:n, 800, FALSE)

x.train <- matrix(as.numeric(unlist(data[train,])), nrow = 800)
x.test <- matrix(as.numeric(unlist(data[-train,])), nrow = 200)

x.train <- x.train[,-c(4,6)]
x.test <- x.test[,-c(4,6)]
head(x.train)
head(x.test)

fit <- Rrbm(x.train)
setHiddenRepresentation(fit, x = 3)  # 3 hidden nodes
setLearningRate(fit, x = 0.01)
summary(fit)

train(fit)

recon.prob <- reconstruct(fit, x.train)
head(recon.prob, 6)
recon <- ifelse(recon.prob >= 0.5, 1, 0)
head(recon)
table(recon, x.train, dnn = c("Predicted", "Observed"))

par(mfrow = c(1,2))
image(x.train, main = "Train")
image(recon, main = "Reconstruction")