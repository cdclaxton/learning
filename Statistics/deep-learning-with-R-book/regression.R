# Regression
# install.packages('Metrics')

library(neuralnet)
require(Metrics)

# Load the Boston data
data("Boston", package="MASS")
boston <- Boston[c("crim", "indus", "nox", "rm", "age", "dis", "tax", "ptratio",
                 "lstat", "medv")]
boston <- scale(boston)

# Check there are no missing values
apply(boston, 2, function(x) sum(is.na(x)))

# Plot
b <- as.data.frame(boston)
pairs(medv ~ ., data = boston)

f <- medv ~ crim + indus + nox + rm + age + dis + tax + ptratio + lstat
set.seed(2016)
n <- nrow(boston)
train <- sample(1:n, 400, FALSE)  # rows to use in training

fit <- neuralnet(f,
                 data = boston[train, ],
                 hidden = c(10,12,20),  # 3 hidden layers
                 algorithm = "rprop+",  # resilient backpropagation with backtracking
                 err.fct = "sse",       # error function (sum of squared errors)
                 act.fct = "logistic",  # activiation function
                 threshold = 0.1,
                 linear.output = TRUE)

plot(fit)

pred <- compute(fit, boston[-train, 1:9])

# Performance
round(cor(pred$net.result, data[-train,10])^2, 6)
mse(cor(pred$net.result, data[-train,10])^2, 6)
rmse(cor(pred$net.result, data[-train,10])^2, 6)

plot(boston[-train,10], pred$net.result)