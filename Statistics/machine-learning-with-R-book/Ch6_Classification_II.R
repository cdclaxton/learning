# Chapter 6: Classification (II) -- Neural Network and SVM
# install.packages('neuralnet')
# install.packages('nnet')
# ------------------------------------------------------------------------------

# Setup
setwd("C:/Users/cdc/OneDrive/Technical/Learning/R/MachineLearningWithR")

# Neural networks and SVMs are black-box methods
# NNs are a computational model that mimics the pattern of the human brain
# SVMs map input data into a high dimension feature space (using a kernel function)
# SVM: find the optimum hyperplane that separates the classes by the maximum margin

## Classifying data with a support vector machine

# SVM: Constructs a hyperplane or set of hyperplanes that maximise the margin
# width between two classes in high-dimensional space.
# Cases that define the hyperplane are support vectors.
# Makes use of regularisation to avoid over-fitting.
# Doesn't suffer from local optimals and collinearity.
# Not suitable for large data.

library(C50)
library(e1071)

# Load the telecoms churn data
data(churn)
churnTrain = churnTrain[, !names(churnTrain) %in% c("state", "area_code", "account_length")]
ind <- sample(2, nrow(churnTrain), replace = TRUE, prob = c(0.7, 0.3))
trainset <- churnTrain[ind == 1, ]
testset <- churnTrain[ind == 2, ]

model <- svm(churn ~ ., data = trainset, kernel = "radial", cost = 1, 
             gamma = 1/ncol(trainset))
summary(model)

## Choosing the cost of a support vector machine

# Cost function controls training errors and margin.
# Small cost -> creates a large margin (soft margin) and allows for more
# misclassifications.
# Large cost -> narrow margin (hard margin), fewer misclassifications.

iris.subset <- subset(iris, select = c("Sepal.Length", "Sepal.Width", "Species"),
                      Species %in% c("setosa", "virginica"))
plot(x = iris.subset$Sepal.Length, y = iris.subset$Sepal.Width,
     col = iris.subset$Species, pch = 19)

# Train the SVM
cost <- 10
svm.model <- svm(Species ~ ., data = iris.subset, kernel = "linear",
                 cost = cost, scale = FALSE)

# Circle the support vectors
indices <- svm.model$index
p <- iris.subset[indices, c(1,2)]
points(p, col = "blue", cex = 2)

# Add a separation line to the plot
w <- t(svm.model$coefs) %*% svm.model$SV
b <- -svm.model$rho
abline(a = -b/w[1,2], b = -w[1,1]/w[1,2], col = "red", lty = 5)

## Visualising an SVM fit

# X - support vector
# O - data point
data("iris")
model.iris <- svm(Species ~ ., iris)
plot(model.iris, iris, Petal.Width ~ Petal.Length,
     slice = list(Sepal.Width = 3, Sepal.Length = 4))

## Predicting labels based on a model trained by a support vector machine
svm.pred <- predict(model, testset[, !names(testset) %in% c("churn")])
svm.table <- table(svm.pred, testset$churn)
svm.table
classAgreement(svm.table)

library(caret)
confusionMatrix(svm.table)

## Train a regression model with SVM

library(car)
data("Quartet")
model.regression <- svm(Quartet$y1 ~ Quartet$x, type = "eps-regression")
predict.y <- predict(model.regression, Quartet$x)
predict.y
plot(Quartet$x, Quartet$y1, pch = 19)
points(Quartet$x, predict.y, pch = 15, col = "red")

## Tuning a support vector machine

# Adjust the gamma and cost configuration
tuned <- tune.svm(churn ~ ., data = trainset, gamma = 10^(-6:-1),
                  cost = 10^(1:2))
summary(tuned)
tuned$best.parameters$gamma
tuned$best.parameters$cost
model.tuned <- svm(churn ~ ., data = trainset, gamma = tuned$best.parameters$gamma,
                   cost = tuned$best.parameters$cost)
summary(model.tuned)

svm.tuned.pred <- predict(model.tuned, testset[, !names(testset) %in% c("churn")])
svm.tuned.table <- table(svm.tuned.pred, testset$churn)
svm.tuned.table
classAgreement(svm.tuned.table)
confusionMatrix(svm.tuned.table)

## Training a neural network with neuralnet

# Neural network: interconnected group of nodes
# Inputs
# Weights -- connection strength
#   > 0 => excitation
#   < 0 => inhibition
# Processing element -- sum up activation values and apply transfer function
# Output
# Input neurons, hidden neurons, output neurons
# NNs can be applied to classification, clustering and prediction
# 'neuralnet' trains a multilayer perceptron for regression
# 
# Advantages of neural networks:
# - detect non-linear relationships between dependent and independent variables
# - can efficiently train large datasets using parallel architecture
# - non-parametric method
# Disadvantages:
# - often converges to a local minimum
# - can overfit if training goes on for too long

data(iris)
ind <- sample(2, nrow(iris), replace = TRUE, prob = c(0.7, 0.3))
trainset <- iris[ind == 1, ]
testset <- iris[ind == 2, ]

library(neuralnet)

# Use one-hot encoding
trainset$setosa <- trainset$Species == "setosa"
trainset$virginica <- trainset$Species == "virginica"
trainset$versicolor <- trainset$Species == "versicolor"

network <- neuralnet(versicolor + virginica + setosa ~ 
                       Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,
                     trainset, hidden = 3)
network
head(network$generalized.weights[[1]])

## Visualising a neural network trained by neuralnet

plot(network)

# Plot the generalised weights
par(mfrow = c(2,2))
gwplot(network, selected.covariate = "Petal.Width")
gwplot(network, selected.covariate = "Sepal.Width")
gwplot(network, selected.covariate = "Petal.Length")
gwplot(network, selected.covariate = "Sepal.Length")

## Predicting labels based on a model trained by neuralnet

net.predict <- compute(network, testset[-5])$net.result
net.prediction <- c("versicolor", "virginica", "setosa")[apply(net.predict, 1, which.max)]
predict.table <- table(testset$Species, net.prediction)
predict.table
classAgreement(predict.table)
confusionMatrix(predict.table)

## Training a neural network with nnet

# Train feedforward neural networks with back propagation
library(nnet)

data(iris)
ind <- sample(2, nrow(iris), replace = TRUE, prob = c(0.7, 0.3))
trainset <- iris[ind == 1, ]
testset <- iris[ind == 2, ]

iris.nn <- nnet(Species ~ ., data = trainset, size = 2, rang = 0.1,
                decay = 5e-4, maxit = 200)
summary(iris.nn)

## Predicting labels based on a model trained by nnet

iris.predict <- predict(iris.nn, testset, type = "class")
nn.table <- table(testset$Species, iris.predict)
confusionMatrix(nn.table)
