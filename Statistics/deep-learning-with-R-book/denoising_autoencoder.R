# Denoising Autoencoder
#
# install.packages('RcppDL')
# install.packages('ltm')

# Clear the workspace
rm(list = ls())

library(RcppDL)
library(ltm)

data(Mobility)
data <- Mobility

set.seed(17)
n <- nrow(data)
sample <- sample(1:n, 1000, FALSE)
data <- as.matrix(Mobility[sample,])

n <- nrow(data)
train <- sample(1:n, 800, FALSE)

x.train <- matrix(as.numeric(unlist(data[train,])), nrow = 800)
x.test <- matrix(as.numeric(unlist(data[-train,])), nrow = 200)

# Remove the response variable (3)
x.train <- x.train[,-3]
x.test <- x.test[,-3]
head(x.train)
head(x.test)

y.train <- data[train, 3]
temp <- ifelse(y.train == 0, 1, 0)
y.train <- cbind(y.train, temp)
head(y.train)

y.test <- data[-train, 3]
temp1 <- ifelse(y.test == 0, 1, 0)
y.test <- cbind(y.test, temp1)
head(y.test)

# Build a stacked autoencoder without any noise
hidden <- c(10,10)
fit <- Rsda(x.train, y.train, hidden)
setCorruptionLevel(fit, x = 0.0)  # set noise to zero
summary(fit)

pretrain(fit)
finetune(fit)

predProb <- predict(fit, x.test)
head(predProb, 6)
head(y.test, 6)

pred1 <- ifelse(predProb[,1] >= 0.5, 1, 0)
table(pred1, y.test[,1], dnn = c("Predicted", "Observed"))

# Re-build the model, this time adding noise
setCorruptionLevel(fit, x = 0.25)  # 25% noise
pretrain(fit)
finetune(fit)
predProb <- predict(fit, x.test)
pred1 <- ifelse(predProb[,1] >= 0.5, 1, 0)
table(pred1, y.test[,1], dnn = c("Predicted", "Observed"))