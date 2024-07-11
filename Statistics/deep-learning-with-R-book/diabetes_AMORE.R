# Pima Indian Diabetes
#
# Setup:
# install.packages('mlbench')
# install.packages('AMORE')

# Clear the workspace
rm(list = ls())

library(mlbench)
library(AMORE)

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

net <- newff(n.neurons = c(6,12,8,1),  # 6 input nodes, 12 hidden, 8 hidden, 1 output
             learning.rate.global = 0.01,
             momentum.global = 0.5,
             error.criterium = "LMLS",  # mean log squared error (robust)
             Stao = NA,
             hidden.layer = "sigmoid",
             output.layer = "purelin",
             method = "ADAPTgdwm") # adaptive gradient descent with momentum

fit <- train(net, 
             P = X, 
             T = Y, 
             error.criterium = "LMLS", 
             report = TRUE, 
             show.step = 100,
             n.shows = 5)

pred <- sign(sim(fit$net, temp[-train,]))

table(pred, sign(temp[-train,7]),
      dnn = c("Predicted", "Observed"))

error.rate <- (1 - sum(pred == sign(temp[-train,7])) / 124)
round(error.rate, 3)