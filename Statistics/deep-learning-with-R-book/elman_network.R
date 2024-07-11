# Elman network
#
# install.packages('RSNNS')
# install.packages('quantmod')

# Clear the workspace
rm(list = ls())

library(ggplot2)
library(RSNNS)
library(quantmod)
library(Metrics)

data("UKLungDeaths", package="datasets")

par(mfrow = c(3,1))
plot(ldeaths, xlab = "Year", ylab = "Number of deaths", main = "Total")
plot(mdeaths, xlab = "Year", ylab = "Number of deaths", main = "Males")
plot(fdeaths, xlab = "Year", ylab = "Number of deaths", main = "Females")

sum(is.na(ldeaths))
class(ldeaths)  # timeseries

par(mfrow = c(3,1))
plot(ldeaths)
x <- density(ldeaths)
plot(x, main = "UK total deaths from lung diseases")
boxplot(ldeaths, col = "cyan", ylab = "Number of deaths per month")

y <- as.ts(ldeaths)
y <- log(y)  # normalise
y <- as.ts(scale(y))  # standardise

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

deaths <- cbind(y, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12)
head(round(deaths, 2), 13)

deaths <- deaths[-(1:12),]  # remove the NAs
n <- nrow(deaths)
set.seed(465)
n.train <- 45
train <- sample(1:n, n.train, FALSE)

inputs <- deaths[,2:13]
outputs <- deaths[,1]

change.num.neurons <- function(n.neurons) {
  fit <- elman(inputs[train],
               outputs[train],
               size = c(8,8),  # two hidden layers, each containing one node
               learnFuncParams = c(0.1),
               maxit = 1000)
  
  #plotIterativeError(fit)
  #summary(fit)
  
  pred <- predict(fit, inputs[-train])
  #plot(outputs[-train], pred)
  
  #cor(outputs[-train], pred)^2
  mse(outputs[-train], pred)
}

df <- data.frame(n.neurons = 1:20,
                 mse = rep(NA,20))
for (i in 1:nrow(df)) {
  df[i,]$mse <- change.num.neurons(df[i,1])
}

ggplot(df, aes(x = n.neurons, y = mse)) + geom_point()

