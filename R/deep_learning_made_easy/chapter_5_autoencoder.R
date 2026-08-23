library(ANN2)
library(dslabs)

# Download the MNIST training and test dataset
mnist <- read_mnist()

# Show the number of test and training samples in the MNIST dataset
cat('Number of training samples:', length(mnist$train$labels), '\n')
cat('Number of test samples:', length(mnist$test$labels), '\n')

# Construct the training data, X
n_training = length(mnist$train$labels)
n_training_to_use = 1000
indices = sample(1:n_training, n_training_to_use, replace=FALSE)
X_train = mnist$train$images[indices,]

# Plot a few images
par(mfrow=c(4,4))
for (j in 1:16) {
	image(1:28, 1:28, matrix(mnist$train$images[indices[j],], nrow=28)[ , 28:1], 
    	col = gray(seq(0, 1, 0.05)), xlab = "", ylab="")
} 

# Train the autocoder neural network
fit <- autoencoder(X_train, hidden.layers=c(25), batch.size=10,
	loss.type='squared', activ.functions='sigmoid', n.epochs=100)
plot(fit)

# Show predictions using the autoencoder
n_test = length(mnist$test$labels)
n_test_to_use = 20
indices = sample(1:n_test, n_test_to_use, replace=FALSE)

pred <- predict(fit, mnist$test$images[indices,])

par(mfrow=c(4,4))
for (j in 1:8) {
	# Plot the original image
	image(1:28, 1:28, matrix(mnist$test$images[indices[j],], nrow=28)[ , 28:1], 
    	col = gray(seq(0, 1, 0.05)), xlab = "", ylab="")

	# Plot the reconstructed image
	m = matrix(as.data.frame(pred)[j,], nrow=28)[ , 28:1]
	mode(m) <- "integer"
	m = pmin(pmax(m, 0), 255)
	image(1:28, 1:28, m, col = gray(seq(0, 1, 0.05)), xlab = "", ylab="")
}
