# Function approximation
# 
# Setup:
# install.packages('neuralnet')

library(ggplot2)
library(neuralnet)

# Generate the ground truth data
set.seed(2016)
attribute <- as.data.frame(sample(seq(-2,2,length=50), 50, replace = FALSE),
                           ncol = 1)
response <- attribute ^ 2
data <- cbind(attribute, response)
colnames(data) <- c("attribute", "response")

# Create a plot
ggplot(data, aes(x = attribute, y = response)) + geom_point()

# Fit a DNN with two hidden layers, each with three neurons
fit <- neuralnet(response ~ attribute, data = data, hidden = c(3,3), threshold = 0.01)
plot(fit)

# Generate the test data
test.data <- as.matrix(sample(seq(-2, 2, length = 20), 20, replace = FALSE), ncol = 1)
pred <- compute(fit, test.data)

result <- cbind(test.data, pred$net.result, test.data^2)
colnames(result) <- c("Attribute", "Prediction", "Actual")
round(result, 4)

result.df <- as.data.frame(result)
ggplot(result.df, aes(x = Attribute)) + 
  geom_point(aes(y = Prediction), color = "red", shape = 0) +
  geom_point(aes(y = Actual), color = "blue")