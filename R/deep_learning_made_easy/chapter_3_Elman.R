require('RSNNS')
require(quantmod)

# Load the data
data("UKLungDeaths", package="datasets")

# Plot the data
par(mfrow=c(3,1))
plot(ldeaths, xlab="Year", ylab="Both sexes", main="Total")
plot(mdeaths, xlab="Year", ylab="Males", main="Males")
plot(fdeaths, xlab="Year", ylab="Females", main="Females")

# Check for missing values
sum(is.na(ldeaths))

# Summarise the ldeaths
par(mfrow=c(3,1))
plot(ldeaths)
x <- density(ldeaths)
plot(x, main="UK total deaths from lung diseases")
polygon(x, col="green", border="black")
boxplot(ldeaths, col="cyan", ylab="Number of deaths per month")

# Transform the data
y <- as.ts(ldeaths)
y <- log(y)
y <- as.ts(scale(y))

# Create the lags
y <- as.zoo(y)
x1 <- Lag(y, k=1)
x2 <- Lag(y, k=2)
x3 <- Lag(y, k=3)
x4 <- Lag(y, k=4)
x5 <- Lag(y, k=5)
x6 <- Lag(y, k=6)
x7 <- Lag(y, k=7)
x8 <- Lag(y, k=8)
x9 <- Lag(y, k=9)
x10 <- Lag(y, k=10)
x11 <- Lag(y, k=11)
x12 <- Lag(y, k=12)

deaths <- cbind(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12)
deaths <- cbind(y, deaths)

head(round(deaths,2),13)

# Remove NAs
deaths <- deaths[-(1:12),]
n = nrow(deaths)

# Split the data
n_train <- 45
train <- sample(1:n, n_train, replace=FALSE)

inputs <- deaths[,2:13]
outputs <- deaths[,1]

# Train the neural network
fit <- elman(inputs[train], outputs[train], size=c(1,1),
	learnFuncParams=c(0.1), maxit=1000)

# Plot the training error
plotIterativeError(fit)

# Summarise the fit
summary(fit)

# Predict
pred <- predict(fit, inputs[-train])
plot(outputs[-train], pred)

# Calculate the squared correlation coefficient
cor(outputs[-train], pred)^2?