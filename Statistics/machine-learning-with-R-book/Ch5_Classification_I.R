# Chapter 5: Classification (I) -- Tree, lazy and probabilistic 
# install.packages('C50')
# install.packages('class')
# ------------------------------------------------------------------------------

# Setup
setwd("C:/Users/cdc/OneDrive/Technical/Learning/R/MachineLearningWithR")

# Classification -- supervised learning method

## Preparing the training and testing datasets

library(C50)
data(churn)
str(churnTrain)
churnTrain = churnTrain[, !names(churnTrain) %in% c("state", "area_code", "account_length")]

# Split the data
set.seed(2)
ind <- sample(2, nrow(churnTrain), replace = TRUE, prob = c(0.7, 0.3))
trainset <- churnTrain[ind == 1, ]
testset <- churnTrain[ind == 2, ]

# Function to split data
split.data <- function(data, p = 0.7, s = 666) {
  set.seed(s)
  n <- dim(data)
  index <- sample(1:n)
  cut.off.index <- floor(n * p)
  train <- data[1:cut.off.index, ]
  test <- data[(cut.off.index + 1):n]
  return(list(train = train, test = test))
}

## Building a classification model with recursive partitioning trees

# Recursive partitioning trees
# - very flexible
# - easy to interpret
# - prone to bias and over-fitting
# - works on classification and regression problems
# - non-parametric

# Non-parametric approach
# Splits by maximising information measures (Gini coefficient)
library(rpart)
churn.rp <- rpart(churn ~ ., data = trainset)  # build the recursive partition tree
printcp(churn.rp)
plotcp(churn.rp)  # plot the cost complexity parameters
summary(churn.rp)

## Visualising a recursive partitioning tree

plot(churn.rp, uniform = TRUE, branch = 0.6, margin = 0.1)
text(churn.rp, all = TRUE, use.n = TRUE)

## Measuring the prediction performance of a recursive partitioning tree

predictions <- predict(churn.rp, testset, type = "class")
table(testset$churn, predictions)

library(caret)
confusionMatrix(table(testset$churn, predictions))

## Pruning a recursive partitioning tree

min(churn.rp$cptable[,"xerror"])  # find the minimum cross-validation error
which.min(min(churn.rp$cptable[,"xerror"]))  # find record with minimum
churn.cp <- churn.rp$cptable[7, "CP"]  # get cost complexity parameter
prune.tree <- prune(churn.rp, cp = churn.cp)
plot(prune.tree, margin = 0.1)
text(prune.tree, all = TRUE, use.n = TRUE)

predictions <- predict(prune.tree, testset, type = "class")
table(testset$churn, predictions)
confusionMatrix(table(testset$churn, predictions))

## Building a classification model with a conditional inference tree

# Conditional inference trees:
# - recursively partition data by performing a univariate split
# - uses significance test procedures to select variables
# - very flexible
# - easy to interpret
# - prone to over-fitting (less prone to bias than recursive partitioning tree)
# - works on classification and regression problems
# - non-parametric

library(party)
ctree.model <- ctree(churn ~ ., data = trainset)

## Visualising a conditional inference tree

plot(ctree.model)

# Simpler model
daycharge.model <- ctree(churn ~ total_day_charge, data = trainset)
plot(daycharge.model)

## Measuring the prediction performance of a conditional inference tree

ctree.predict <- predict(ctree.model, testset)
table(ctree.predict, testset$churn)
confusionMatrix(table(ctree.predict, testset$churn))
tr <- treeresponse(ctree.model, newdata = testset[1:5,])

## Classifying data with k-nearest neighbour classifier

# k-NN:
# - non-parametric (don't have to make assumptions as to the data distribution)
# - lazy learning (cost of learning is zero)
# - distances: Euclidean; Manhattan
# - expensive for large datasets
# - reduce the number of dimensions for a high dimension problem
# - hard to interpret the classified result

library(class)

# All variables must be numeric
levels(trainset$international_plan) <- list("0" = "no", "1" = "yes")
levels(trainset$voice_mail_plan) <- list("0" = "no", "1" = "yes")
levels(testset$international_plan) <- list("0" = "no", "1" = "yes")
levels(testset$voice_mail_plan) <- list("0" = "no", "1" = "yes")

churn.knn <- knn(trainset[, !names(trainset) %in% c("churn")],
                 testset[, !names(testset) %in% c("churn")],
                 trainset$churn, k = 3)
summary(churn.knn)
table(testset$churn, churn.knn)
confusionMatrix(table(testset$churn, churn.knn))

## Classifying data with logistic regression

# Logistic regression:
# - form of probabilistic statistical classification model
# - logit function to estimate the outcome probability
# - easy to interpret
# - provides a confidence interval for the result
# - can quickly update the classification model to incorporate new data
# - suffers from multicollinearity
# - explanatory variables must be independent
# - doesn't handle missing values of continuous variables
# - sensitive to extreme values of continuous variables

fit <- glm(churn ~ ., data = trainset, family = binomial)
summary(fit)

# Only use significant variables
fit <- glm(churn ~ international_plan + voice_mail_plan + total_intl_calls + 
             number_customer_service_calls, 
           data = trainset, family = binomial)
summary(fit)

pred <- predict(fit, testset, type = "response")
output.class <- pred > 0.5
summary(output.class)
tb <- table(testset$churn, output.class)

churn.mod <- ifelse(testset$churn == "yes", 1, 0)
pred.class <- churn.mod
pred.class[pred <= 0.5] = 1 - pred.class[pred <= 0.5]
ctb <- table(churn.mod, pred.class)
ctb
confusionMatrix(ctb)

## Classifying data with Naive Bayes classifier

# Naive-Bayer classifier:
# - probability-based classifier
# - based on applying Bayes' theorem
# - strong independence assumption
# - assumes all features are equally important
# - suitable when training set is small
# - can deal with some noisy and missing data
# - prone to bias when the number of training sets increases

library(e1071)
classifier <- naiveBayes(trainset[, !names(trainset) %in% c("churn")],
                         trainset$churn)

# Generate the classification table
bayes.table <- table(predict(classifier, 
                             testset[, !names(testset) %in% c("churn")]),
                     testset$churn)
confusionMatrix(bayes.table)