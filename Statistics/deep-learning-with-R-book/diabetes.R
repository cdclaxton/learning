# Pima Indian Diabetes
#
# Setup:
# install.packages('mlbench')
# install.packages('RSNNS')

# Clear the workspace
rm(list = ls())

library(mlbench)
library(RSNNS)

# Load the diabetes data
data("PimaIndiansDiabetes2", package="mlbench")
str(PimaIndiansDiabetes2)

# Check the number of entries that are NA
sapply(PimaIndiansDiabetes2, function(x) sum(is.na(x)))

# Clean up the data
temp <- PimaIndiansDiabetes2
temp$insulin <- NULL
temp$triceps <- NULL
temp <- na.omit(temp)

# Change the type of the target variable
y <- temp$diabetes
levels(y) <- c("0", "1")
y <- as.numeric(as.character(y))

# Remove the old target variable and add in the modified before scaling
temp$diabetes <- NULL
temp <- cbind(temp, y)
temp <- scale(temp)

class(temp)

summary(temp)

# Create the training dataset
set.seed(2016)
n <- nrow(temp)
n.train <- 600
n.test <- n - n.train
train <- sample(1:n, n.train, FALSE)

X <- temp[train, 1:6]
Y <- temp[train, 7]

fitMLP <- mlp(x = X, y = Y,
              size = c(12,8),  # two hidden layers
              maxit = 1000,
              initFunc = "Randomize_Weights",
              initFuncParams = c(-0.3, 0.3),
              learnFunc = "Std_Backpropagation",
              learnFuncParams = c(0.2, 0),
              updateFunc = "Topological_Order",
              updateFuncParams = c(0),
              hiddenActFunc = "Act_Logistic",  # logistic activation function
              shufflePatterns = TRUE,
              linOut = TRUE)  # linear activation function in output neuron

predMLP <- sign(predict(fitMLP, temp[-train, 1:6]))

table(predMLP, sign(temp[-train,7]),
      dnn = c("Predicted", "Observed"))

error.rate <- (1 - sum(predMLP == sign(temp[-train,7])) / 124)
round(error.rate, 3)