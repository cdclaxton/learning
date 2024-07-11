# Jordan networks

# Clear the workspace
rm(list = ls())

library(RSNNS)
library(quantmod)

data("nottem", package = "datasets")

plot(nottem)

y <- as.ts(nottem)
y <- as.ts(scale(log(y)))

y <- as.zoo(y)
x1 <- Lag(y, k = 1)
x2 <- Lag(y, k = 2)
x3 <- Lag(y, k = 3)
x4 <- Lag(y, k = 4)
x5 <- Lag(y, k = 5)
x6 <- Lag(y, k = 6)
x7 <- Lag(y, k = 7)
x8 <- Lag(y, k = 8)
x9 <- Lag(y, k = 9)
x10 <- Lag(y, k = 10)
x11 <- Lag(y, k = 11)
x12 <- Lag(y, k = 12)

temp <- cbind(y, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12)
temp <- temp[-(1:12),]

plot(temp)

n <- nrow(temp)
set.seed(465)
n.train <- 190
train <- sample(1:n, n.train, FALSE)

inputs <- temp[,2:13]
outputs <- temp[,1]

fit <- jordan(inputs[train],
              outputs[train],
              size = 2,
              learnFuncParams = c(0.01),
              maxit = 1000)

plotIterativeError(fit)

pred <- predict(fit, inputs[-train])
cor(outputs[-train], pred)^2