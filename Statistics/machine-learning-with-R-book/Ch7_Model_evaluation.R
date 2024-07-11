# Chapter 7: Model evaluation
# install.packages('rminer')
# install.packages('ROCR')
# install.packages('pROC')
# ------------------------------------------------------------------------------

# Setup
setwd("C:/Users/Christopher/OneDrive/Technical/Learning/R/MachineLearningWithR")

## Estimating model performance with k-fold cross-validation

# Overcomes the problem of over-fitting
# Doesn't use the entire dataset to build the model
# Split data into training and test sets
# Use the average of n accuracies to predict model performance
# Train on k-1 folds and test using the remaining fold

# Load the telecoms churn data
library(C50)
data(churn)
churnTrain = churnTrain[, !names(churnTrain) %in% c("state", "area_code", "account_length")]

n.breaks <- 10
ind <- cut(1:nrow(churnTrain), breaks = n.breaks, labels = FALSE)
accuracies <- c()
for (i in 1:n.breaks) {
  fit <- svm(churn ~ ., churnTrain[ind != i, ])
  predictions <- predict(fit, churnTrain[ind == i, !names(churnTrain) %in% c("churn")])
  correct_count <- sum(predictions == churnTrain[ind == i, c("churn")])
  accuracies <- append(correct_count / nrow(churnTrain[ind == i, ]), accuracies)
}
accuracies
mean(accuracies)

## Performing cross-validation with the e1071 package

# Retrieve the minimum estimation error using cross-validation
library(e1071)
ind <- sample(2, nrow(churnTrain), replace = TRUE, prob = c(0.7, 0.3))
trainset <- churnTrain[ind == 1, ]
testset <- churnTrain[ind == 2, ]
tuned <- tune.svm(churn ~ ., data = trainset, gamma = 10^-2, cost = 10^2, 
                  tunecontrol = tune.control(cross=10))
summary(tuned)
tuned$performances
svmfit <- tuned$best.model
table(trainset[,c("churn")], predict(svmfit))

## Performing cross-validation with the caret package

library(caret)
# Perform repeated k-fold cross-validation (test stability of the model)
control <- trainControl(method = "repeatedcv", number = 10, repeats = 3)
model <- train(churn ~ ., data = trainset, method = "rpart", preProcess = "scale",
               trControl = control)
model

## Ranking variable importance with the caret package

# After building a supervised learning model, the importance of the features can be
# estimated
# Employs a sensitivity analysis to measure the effect on the output

importance <- varImp(model, scale = FALSE)
importance
plot(importance)

## Ranking the variable importance with the rminer package

library(rminer)
model <- fit(churn ~ ., trainset, model = "svm")
vImp <- Importance(model, trainset, method = "sensv")
l = list(runs = 1, sens = t(vImp$imp), sresponses = vImp$sresponses)
mgraph(l, graph = "IMP", leg = names(trainset), col = "gray", Grid = 10)

## Finding highly correlated features with the caret package

# Some regression or classification algorithms perform better if highly correlated
# attributes are removed.

# Remove features that are not coded in numeric characters
new.train <- trainset[, !names(churnTrain) %in% 
                        c("churn", "international_plan", "voice_mail_plan")]
cor.mat <- cor(new.train)
highly.correlated <- findCorrelation(cor.mat, cutoff = 0.75)
names(new.train)[highly.correlated]

## Selecting features using the caret package

# Search for the subset of features with the minimised predictive errors

churnTrain = churnTrain[, !names(churnTrain) %in% c("state", "area_code", "account_length")]

# Transform the international plan feature (transform factor coded attributes
# into multiple binary attributes)
intl.plan <- model.matrix(~ churnTrain$international_plan - 1,
                          data = data.frame(churnTrain$international_plan))
colnames(intl.plan) <- c("international_planno" = "intl_no",
                         "international_planyes" = "intl_yes")

# Transform the voice mail feature
voice.plan <- model.matrix(~ churnTrain$voice_mail_plan - 1,
                           data = data.frame(churnTrain$voice_mail_plan))
colnames(voice.plan) <- c("voice_mail_planno" = "voice_no",
                          "voice_mail_planyes" = "voice_yes")

# Remove attributes
churnTrain$international_plan <- NULL
churnTrain$voice_mail_plan <- NULL
churnTrain <- cbind(churnTrain, intl.plan, voice.plan)

ind <- sample(2, nrow(churnTrain), replace = TRUE, prob = c(0.7, 0.3))
trainset <- churnTrain[ind == 1, ]
testset <- churnTrain[ind == 2, ]

# Use linear discriminant analysis
lda.control <- rfeControl(functions = ldaFuncs, method = "cv")

# Perform backward feature selection
lda.profile <- rfe(trainset[, !names(trainset) %in% c("churn")],
                   trainset[, c("churn")], sizes = c(1:18),
                   rfeControl = lda.control)
lda.profile

plot(lda.profile, type = c("o", "g"))

# Examine the best subset of variables
lda.profile$optVariables

lda.profile$fit

# Calculate the performance across resamples
postResample(predict(lda.profile, testset[, !names(testset) %in% c("churn")]),
             testset[, c("churn")])

## Measuring the performance of the regression model

# Measure distance from the predicted output and the actual output
# RMSE -- Root Mean Square Error
# RSE -- Relative Square Error
# R-Square = 1 - RSE

library(car)
data("Quartet")
plot(Quartet$x, Quartet$y3)
lmfit <- lm(Quartet$y3 ~ Quartet$x)
abline(lmfit, col = "red")

predicted <- predict(lmfit, newdata = Quartet[c("x")])
actual <- Quartet$y3
rmse <- (mean((predicted - actual)^2))^0.5
rmse

mu <- mean(actual)
rse <- mean((predicted - actual)^2) / mean((mu - actual)^2)
rse

rsquare <- 1 - rse
rsquare

library(MASS)
plot(Quartet$x, Quartet$y3)
rlmfit <- rlm(Quartet$y3 ~ Quartet$x)
abline(rlmfit, col = "red")

predicted <- predict(rlmfit, newdata = Quartet[c("x")])
actual <- Quartet$y3
rmse <- (mean((predicted - actual)^2))^0.5
rmse


mu <- mean(actual)
rse <- mean((predicted - actual)^2) / mean((mu - actual)^2)
rse

rsquare <- 1 - rse
rsquare

# Perform cross-validation on a linear regression model
tune(lm, y3 ~ x, data = Quartet)

## Measuring prediction performance with a confusion matrix

svm.model <- train(churn ~ ., data = trainset, method = "svmRadial")
svm.pred <- predict(svm.model, testset[, !names(testset) %in% c("churn")])
table(svm.pred, testset[,c("churn")])
confusionMatrix(svm.pred, testset[,c("churn")])

## Measurng prediction performane using ROCR

# Receiver Operating Characteristic (ROC):
# - illustrates the performance of a binary classifier
# - plots false positive rate vs. true positive rate for different cut points
# - use to calculate Area Under Curve (AUC) to measure performance

library(ROCR)
svmfit <- svm(churn ~ ., data = trainset, prob = TRUE)
pred <- predict(svmfit, testset[, !names(testset) %in% c("churn")], probability = TRUE)
pred.prob <- attr(pred, "probabilities")
pred.to.roc <- pred.prob[, 2]
pred.rocr <- prediction(pred.to.roc, testset$churn)
perf.rocr <- performance(pred.rocr, measure = "auc", x.measure = "cutoff")
perf.tpr.rocr <- performance(pred.rocr, "tpr", "fpr")
plot(perf.tpr.rocr, colorize = TRUE, main = paste("AUC:", (perf.rocr@y.values)))

## Comparing an ROC curve using the caret package

library(caret)
library(pROC)
control <- trainControl(method = "repeatedcv", number = 10, repeats = 3,
                        classProbs = TRUE, summaryFunction = twoClassSummary)
glm.model <- train(churn ~ ., data = trainset, method = "glm", metric = "ROC",
                   trControl = control)
svm.model <- train(churn ~ ., data = trainset, method = "svmRadial", metric = "ROC",
                   trControl = control)
rpart.model <- train(churn ~ ., data = trainset, method = "rpart", metric = "ROC",
                   trControl = control)

glm.probs <- predict(glm.model, testset[, !names(testset) %in% c("churn")], type = "prob")
svm.probs <- predict(svm.model, testset[, !names(testset) %in% c("churn")], type = "prob")
rpart.probs <- predict(rpart.model, testset[, !names(testset) %in% c("churn")], type = "prob")

glm.roc <- roc(response = testset[, c("churn")], 
               predictor = glm.probs$yes,
               levels = levels(testset[, c("churn")]))
plot(glm.roc, type = "S", col = "red")

svm.roc <- roc(response = testset[, c("churn")], 
               predictor = svm.probs$yes,
               levels = levels(testset[, c("churn")]))
plot(svm.roc, add = TRUE, col = "green")

rpart.roc <- roc(response = testset[, c("churn")], 
                 predictor = rpart.probs$yes,
                 levels = levels(testset[, c("churn")]))
plot(rpart.roc, add = TRUE, col = "blue")

## Measuring performance differences between models with the caret package

cv.values <- resamples(list(glm = glm.model, 
                            svm = svm.model,
                            rpart = rpart.model))
summary(cv.values)
dotplot(cv.values, metric = "ROC")
bwplot(cv.values, layout = c(3,1))
densityplot(cv.values, metric = "ROC")
splom(cv.values)
xyplot(cv.values)