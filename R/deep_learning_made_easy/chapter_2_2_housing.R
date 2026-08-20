library('ggplot2')
library('neuralnet')
require(Metrics)

# Load the data
data("Boston", package="MASS")
data <- Boston

# Retain the required attributes
keeps <- c("crim", "indus", "nox", "rm" ,
    "age" , "dis" , "tax" ,"ptratio" , "lstat", "medv")
data <- data[keeps]

# Scale the data to a z-score
data <- as.data.frame(scale(data))

# Check if there are any missing values
apply(data, 2, function(x) sum(is.na(x)))

# Specify the formula
f <- medv ~ crim + indus + nox + rm + age + dis + tax + ptratio + lstat

# Number of rows in the data
n = nrow(data)

# Determine the training rows
train <- sample(1:n, 400, replace=FALSE)

# Fit the neural network with two hidden layers
fit <- neuralnet(f, data=data[train,], hidden=c(5, 10),
     linear.output=TRUE)

# Perform prediction on the test set
pred <- compute(fit, data[-train, 1:9])

# Calculate the mean squared error
mse(data[-train, 10], pred$net.result)

# Plot the predicted and the actual values
df <- cbind(data[-train, 10], pred$net.result)
colnames(df) <- c("Actual", "Predicted")
df <- as.data.frame(df)

ggplot(df, aes(x=Actual, y=Predicted)) +
    geom_point() +
    geom_abline(slope=1, intercept=0)