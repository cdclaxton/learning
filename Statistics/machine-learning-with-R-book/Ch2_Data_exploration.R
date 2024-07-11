# Chapter 2: Data exploration with RMS Titanic
#
# install.packages('Amelia')
# install.packages('vcd')
# install.packages('party')
# install.packages('caret')
# install.packages('ROCR')
# ------------------------------------------------------------------------------

# Exploration process:
# 1. Ask questions
# 2. Data collection
# 3. Data munging -- parse, sort, merge, filter, missing value completion
# 4. Basic exploratory data analysis
# 5. Advanced exploratory data analysis
# 6. Model assessment

# Setup
setwd("C:/Users/cdc/OneDrive/Technical/Learning/R/MachineLearningWithR")

## Reading Titanice data from CSV

# Read the tranining data
train.data <- read.csv("./data/titanic_train.csv", na.strings = c("NA",""))

## Converting types on character variables

train.data$Survived <- factor(train.data$Survived)
train.data$Pclass <- factor(train.data$Pclass)

# Nominal -- label variables (e.g. gender, name)
# Ordinal -- measures of non-numeric concepts (e.g. satisfaction)
# Interval -- numeric scale, find order and difference (e.g. temperature in Celsius)
# Ratio -- ratio of magnitude to a unit magnitude (e.g. weight, height)

## Detecting missing values

# To find the number of missing values
sum(is.na(train.data$Age) == TRUE)

# Percentage of missing values
100 * sum(is.na(train.data$Age) == TRUE) / length(train.data$Age)

# To get the proportion of missing values for each of the attributes
sapply(train.data, function(x) { sum(is.na(x) == TRUE) / length(x) })

# Visualise the missing values
# Missing values for Cabin, Age and Embarked
require(Amelia)
missmap(train.data, main = "Missing Map")

## Imputing missing values

# Get counts of the embarkation port
table(train.data$Embarked, useNA = "always")

# Assign the 2 values the most probable port (S)
train.data$Embarked[which(is.na(train.data$Embarked))] <- "S"
table(train.data$Embarked, useNA = "always")

# Get counts of the passengers' titles
train.data$Name <- as.character(train.data$Name)
tokens <- unlist(strsplit(train.data$Name, "\\s+"))  # all tokens
title.indices <- grep('\\.', tokens)  # indices of tokens with a .
title.tokens <- tokens[title.indices]
table.titles <- sort(table(title.tokens), decreasing = TRUE)

# Get a count of the titles that have missing ages
library(stringr)
titles <- str_match(train.data$Name, "[a-zA-Z]+\\.")
age.title <- cbind(train.data$Age, titles)
table(age.title[is.na(age.title[,1]), 2])

# Impute the age by assigning the mean value of the title
age.title.no.nas <- age.title[!is.na(age.title[,1]), ]
age.title.no.nas <- data.frame(age = age.title.no.nas[,1],
                               title = age.title.no.nas[,2])
mean.age <- aggregate(as.numeric(age.title.no.nas[,1]), 
                      by = list(age.title.no.nas$title), FUN = mean)

train.data$Age[grepl("Mr\\.", train.data$Name) & is.na(train.data$Age)] <- 
  mean.age[mean.age$Group.1 == "Mr.", 2]
train.data$Age[grepl("Mrs\\.", train.data$Name) & is.na(train.data$Age)] <- 
  mean.age[mean.age$Group.1 == "Mrs.", 2]
train.data$Age[grepl("Dr\\.", train.data$Name) & is.na(train.data$Age)] <- 
  mean.age[mean.age$Group.1 == "Dr.", 2]
train.data$Age[grepl("Miss\\.", train.data$Name) & is.na(train.data$Age)] <- 
  mean.age[mean.age$Group.1 == "Miss.", 2]
train.data$Age[grepl("Master\\.", train.data$Name) & is.na(train.data$Age)] <- 
  mean.age[mean.age$Group.1 == "Master.", 2]

## Exploring and visualising data

barplot(table(train.data$Survived), main = "Passenger Survival",
        names = c("Perished", "Survived"))

barplot(table(train.data$Pclass), main = "Passenger Class",
        names = c("first", "second", "third"))

barplot(table(train.data$Sex), main = "Passenger Gender")

hist(train.data$Age, main = "Passenger Age", xlab = "Age")

barplot(table(train.data$SibSp), main = "Number of Siblings/Spouses Aboard")

barplot(table(train.data$Parch), main = "Number of Parents/Children Aboard")

hist(train.data$Fare, main = "Passenger Fare", xlab = "Fare")

barplot(table(train.data$Embarked), main = "Port of Embarkation")

# Survival by gender
counts <- table(train.data$Survived, train.data$Sex)
barplot(counts, col = c("darkblue", "red"), legend = c("Perished", "Survived"),
        main = "Passenger Survival by Gender")

# Survival by passenger class
counts <- table(train.data$Survived, train.data$Pclass)
rownames(counts) <- c("Perished", "Survived")
colnames(counts) <- c("first", "second", "third")
barplot(counts, col = c("darkblue", "red"), legend = rownames(counts),
        main = "Survival by class")

# Gender composition by class
counts <- table(train.data$Sex, train.data$Pclass)
colnames(counts) <- c("first", "second", "third")
barplot(counts, col = c("darkblue", "red"), legend = rownames(counts),
        main = "Passenger Gender by Class")

# Histogram of passenger ages
hist(train.data$Age[which(train.data$Survived == "0")], 
     main = "Passenger Age", xlab = "Age", col = "blue", breaks = seq(0,80,2))
hist(train.data$Age[which(train.data$Survived == "1")], 
     col = "red", breaks = seq(0,80,2), add = TRUE)

# Relationship between Age and Survival
boxplot(train.data$Age ~ train.data$Survived, main = "Passenger Survival by Age",
        xlab = "Survived", ylab = "Age")

# Survival by Age group
child <- train.data[train.data$Age < 13, ]
youth <- train.data[train.data$Age >= 13 & train.data$Age <= 19, ]
adult <- train.data[train.data$Age >= 20 & train.data$Age < 65, ]
senior <- train.data[train.data$Age >= 65, ]

sum(child$Survived == 1) / nrow(child)
sum(youth$Survived == 1) / nrow(youth)
sum(adult$Survived == 1) / nrow(adult)
sum(senior$Survived == 1) / nrow(senior)

library(vcd)
mosaicplot(train.data$Pclass ~ train.data$Survived, 
           main = "Passenger Survival by Class", color = TRUE,
           xlab = "Passenger Class", ylab = "Survived")

## Predicting passenger survival with a decision tree

# Function to split data into training and test sets
split.data <- function(data, p = 0.7, s = 123) {
  set.seed(s)
  index <- sample(1:dim(data)[1])  # vector of random indices
  cut.off.index <- floor(dim(data)[1] * p)
  train <- data[1:cut.off.index, ]
  test <- data[(cut.off.index + 1):dim(data)[1], ]
  return(list(train = train, test = test))
}

sets <- split.data(train.data, p = 0.7)

require(party)
train.ctree <- ctree(Survived ~ Pclass + Sex + Age + SibSp + Fare + Parch + Embarked, 
                     data = sets$train)
plot(train.ctree, main = "Conditional inference tree of Titanic dataset")

# Support Vector Machine
require('e1071')
svm.model <- svm(Survived ~ Pclass + Sex + Age + SibSp + Fare + Parch + Embarked, 
                 data = sets$train, probability = TRUE)

## Validating the power of prediction with a confusion matrix
require(caret)
ctree.predict <- predict(train.ctree, sets$test)

confusionMatrix(ctree.predict, sets$test$Survived)

## Assessing performance with an ROC curve
require(ROCR)
ctree.prob <- 1 - unlist(treeresponse(train.ctree, sets$test), use.names = FALSE)[seq(1,nrow(sets$test)*2,2)]
ctree.rocr <- prediction(ctree.prob, sets$test$Survived)
ctree.perf <- performance(ctree.rocr, "tpr", "fpr")
ctree.auc <- performance(ctree.rocr, measure = "auc", x.measure = "cutoff")
plot(ctree.perf, col = 2, colorize = TRUE, main = paste("AUC:",ctree.auc@y.values))
