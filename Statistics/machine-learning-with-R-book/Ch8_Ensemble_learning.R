# Chapter 8: Ensemble learning
# install.packages('adabag')
# install.packages('ipred')
# install.packages('mboost')
# install.packages('pROC')
# install.packages('gbm')
# install.packages('randomForest')
# ------------------------------------------------------------------------------

# Setup
setwd("C:/Users/Christopher/OneDrive/Technical/Learning/R/MachineLearningWithR")

## Introduction

# Ensemble learning:
# - method to combine results produced by different learners
# - aim: produce a better classification or regression result
# - single classifier is likely to be imperfect
# - average the results from different classifier (using voting)
# - Bagging:
#   * voting method
#   * uses Bootstrap to generate different training sets (to make different base learners)
#   * uses a combination of the different learners
# - Boosting:
#   * constructst the base learners in sequence
#   * each successive learner is built for the residuals of the previous learner
# - Random forest:
#   * votes from different classification trees
#   * uses the majority vote or average output for regression

## Classifying data with the bagging method

# Bootstrap aggregating -- bagging

# Load the telecoms churn data
library(C50)
data(churn)
churnTrain = churnTrain[, !names(churnTrain) %in% c("state", "area_code", "account_length")]
ind <- sample(2, nrow(churnTrain), replace = TRUE, prob = c(0.7, 0.3))
trainset <- churnTrain[ind == 1, ]
testset <- churnTrain[ind == 2, ]

library(adabag)
churn.bagging <- bagging(churn ~ ., data = trainset, mfinal = 10)
churn.bagging$importance
churn.pred.bagging <- predict.bagging(churn.bagging, newdata = testset)
churn.pred.bagging$confusion
churn.pred.bagging$error

library(ipred)
churn.bagging <- bagging(churn ~ ., data = trainset, coob = TRUE)
churn.bagging
mean(predict(churn.bagging) != trainset$churn)
churn.prediction <- predict(churn.bagging, newdata = testset, type = "class")
prediction.table <- table(churn.prediction, testset$churn)
prediction.table

## Performing cross-validation with the bagging method

# Perform k-fold cross validation
churn.bagging.cv <- bagging.cv(churn ~ ., v = 10, data = trainset, mfinal = 10)
churn.bagging.cv$confusion
churn.bagging.cv$error

## Classifying data with the boosting method

# Starts with a simple or weak classifier and gradually improves it
# Reweights misclassified samples
# Weight is assigned to each point
# Decrease weight if the point is correctly classified, otherwise increase it
# Weighted average of each tree's prediction
# Bagging combines independent classifiers
# Boosting performs an iterative process to reduce errors

churn.boost <- boosting(churn ~ ., data = trainset, mfinal = 10,
                        coeflearn = "Freund", boos = FALSE, 
                        control = rpart.control(maxdepth = 3))
churn.boost.pred <- predict.boosting(churn.boost, newdata = testset)
churn.boost.pred$confusion
churn.boost.pred$error

library(mboost)
library(pROC)
ctrl <- trainControl(method = "repeatedcv", repeats = 1, classProbs = TRUE,
                     summaryFunction = twoClassSummary)
ada.train <- train(churn ~ ., data = trainset, method = "ada", metric = "ROC",
                   trControl = ctrl)
ada.train$result
plot(ada.train)
ada.predict <- predict(ada.train, testset, "prob")
ada.predict.result <- ifelse(ada.predict[1] > 0.5, "yes", "no")
table(testset$churn, ada.predict.result)

## Performing cross-validation with the boosting method

# 10-fold cross-validation, 5 iterations, complexity parameter of 0.01
churn.boost.cv <- boosting.cv(churn ~ ., v = 10, data = trainset,
                              mfinal = 5, control = rpart.control(cp = 0.01))
churn.boost.cv$confusion
churn.boost.cv$error

## Classifying data with gradient boosting

library(gbm)
trainset$churn = ifelse(trainset$churn == "yes", 1, 0)
churn.gbm <- gbm(formula = churn ~ ., 
                 distribution = "bernoulli", data = trainset,
                 n.trees = 1000, interaction.depth = 7,
                 shrinkage = 0.01, cv.folds = 3)
summary(churn.gbm)

churn.iter <- gbm.perf(churn.gbm, method = "cv")
churn.predict <- predict(churn.gbm, testset, n.trees = churn.iter)
str(churn.predict)

churn.roc <- roc(testset$churn, churn.predict)
plot(churn.roc)
coords(churn.roc, "best")
churn.predict.class <- ifelse(churn.predict > coords(churn.roc, "best")["threshold"],
                              "yes", "no")
table(testset$churn, churn.predict.class)

## Classifying data with random forest

# Grows multiple decision trees
# Each decision tree outputs its own prediction results
# Uses a voting mechanism to select the most voted class
# Prone to overfit noisy data

data(churn)
churnTrain = churnTrain[, !names(churnTrain) %in% c("state", "area_code", "account_length")]
ind <- sample(2, nrow(churnTrain), replace = TRUE, prob = c(0.7, 0.3))
trainset <- churnTrain[ind == 1, ]
testset <- churnTrain[ind == 2, ]

library(randomForest)
churn.rf <- randomForest(churn ~ ., data = trainset, importance = TRUE)
churn.prediction <- predict(churn.rf, testset)
table(churn.prediction, testset$churn)
plot(churn.rf)
importance(churn.rf)
varImpPlot(churn.rf)

margins.rf <- margin(churn.rf, trainset)
plot(margins.rf)
hist(margins.rf, main = "Margins of Random Forest for churn dataset")