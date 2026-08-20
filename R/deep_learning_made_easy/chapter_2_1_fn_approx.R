library("ggplot2")
library("neuralnet")

# Generate a shuffled list of x
attribute <- as.data.frame(
    sample(seq(-2, 2, length = 50), 50, replace = FALSE),
    ncol = 1
)

# Calculate y = x^2
response <- attribute^2

# Create a dataframe
data <- cbind(attribute, response)
colnames(data) <- c("attribute", "response")

# Train a neural network
fit <- neuralnet(response ~ attribute, data = data, hidden = c(3, 3), threshold = 0.01)

# Test the neural network
testdata <- as.matrix(seq(-2, 2, length = 20), ncol = 1)
pred <- compute(fit, testdata)
result <- cbind(testdata, pred$net.result, testdata^2)
colnames(result) <- c("Attribute", "Prediction", "Actual")

# Plot the predicted and the actual results
result <- as.data.frame(result)
ggplot(result, aes(Attribute)) +
    geom_line(aes(y = Prediction, colour = "Prediction")) +
    geom_point(aes(y = Prediction, colour = "Prediction")) +
    geom_line(aes(y = Actual, color = "Actual")) +
    geom_point(aes(y = Actual, colour = "Actual"))
