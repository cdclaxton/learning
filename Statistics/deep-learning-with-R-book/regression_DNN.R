# Regression with the deepnet package
# install.packages('deepnet')

require(deepnet)
require(Metrics)

# Load the data
data("Boston", package="MASS")
boston <- Boston[c("crim", "indus", "nox", "rm", "age", "dis", "tax", "ptratio",
                   "lstat", "medv")]
boston <- scale(boston)

# Select the training data
n <- nrow(boston)
train <- sample(1:n, 400, FALSE)  # rows to use in training

set.seed(2016)
X <- boston[train, 1:9]
Y <- boston[train, 10]

fit <- nn.train(x = X, y = Y,
                initW = NULL,  # neuron weights start (set to random with NULL)
                initB = NULL,  # neuron biases start (set to random with NULL)
                hidden = c(10, 12, 20),  # three layers with 10, 12 and 20 neurons
                learningrate = 0.58,  # convergence rate (for backpropagation)
                momentum = 0.74,      # add weighted average of past gradients
                learningrate_scale = 1,
                activationfun = "sigm",  # activation function (logistic)
                output = "linear",
                numepochs = 970,
                batchsize = 60,
                hidden_dropout = 0,
                visible_dropout = 0)

Xtest <- data[-train, 1:9]
pred <- nn.predict(fit, Xtest)

# Performance
round(cor(pred, data[-train,10])^2, 6)
mse(cor(pred, data[-train,10])^2, 6)
rmse(cor(pred, data[-train,10])^2, 6)