# Deep Belief Networks
#

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

y <- apply(cbind(data[,4], data[,6]), 1, max, na.rm = TRUE)

y.train <- as.numeric(y[train])
temp <- ifelse(y.train == 0, 1, 0)
y.train <- cbind(y.train, temp)
head(y.train)

y.test <- as.numeric(y[-train])
temp1 <- ifelse(y.test == 0, 1, 0)
y.test <- cbind(y.test, temp1)
head(y.test)

nrow(y.train)
nrow(y.test)

hidden <- c(12, 10)  # 2 hidden layers
fit <- Rdbn(x.train, y.train, hidden)
summary(fit)

pretrain(fit)
finetune(fit)

pred.prob <- predict(fit, x.test)
head(pred.prob, 6)
pred1 <- ifelse(pred.prob[,1] >= 0.5, 1, 0)
table(pred1, y.test[,1], dnn = c("Predicted", "Observed"))
