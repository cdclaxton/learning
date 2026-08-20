library('ggplot2')
library('deepnet')
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

X = data.matrix(data[train, 1:9])
Y = data[train, 10]

# Train the neural network
fit <- nn.train(x=X, y=Y, initW = NULL, initB = NULL,
    hidden = c(3, 3), activationfun = "sigm", learningrate = 0.58,
    momentum = 0.74, learningrate_scale = 1, output = "linear", 
    numepochs = 1000, batchsize = 50, hidden_dropout = 0, visible_dropout = 0)

Xtest <- data[-train, 1:9]
pred <- nn.predict(fit, Xtest)

# Calculate the mean squared error
mse(data[-train, 10], pred)

# Plot the predicted and the actual values
df <- cbind(data[-train, 10], pred)
colnames(df) <- c("Actual", "Predicted")
df <- as.data.frame(df)

ggplot(df, aes(x=Actual, y=Predicted)) +
    geom_point() +
    geom_abline(slope=1, intercept=0)