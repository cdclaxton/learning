# Body fat
# 
# install.packages(c('ggplot2', TH.data', 'neuralnet', 'Metrics', 'deepnet'))

# Clear the workspace
rm(list = ls())

library(ggplot2)
library(TH.data)
library(neuralnet)
library(Metrics)
library(deepnet)

# Load the data
data("bodyfat", package = "TH.data")

# Kernel density plot of waist and hip circumference
ggplot(bodyfat) + 
  geom_density(aes(waistcirc), color = "red",  fill = "red", alpha = 0.1) + 
  geom_density(aes(hipcirc), color = "blue", fill = "blue", alpha = 0.1) +
  labs(x = "measurement") +
  xlim(50, 150)

# Age distribution
qplot(bodyfat$age, geom="histogram", binwidth = 2)

# Training data
set.seed(2016)
train <- sample(1:nrow(bodyfat), 50, FALSE)

# Scale
scale.bodyfat <- as.data.frame(scale(log(bodyfat)))
f <- waistcirc + hipcirc ~ DEXfat + age + elbowbreadth + kneebreadth +
  anthro3a + anthro3b + anthro3c + anthro4

fit <- neuralnet(f,
                 data = scale.bodyfat[train, ],
                 hidden = c(8,4),
                 threshold = 0.1,
                 err.fct = "sse",
                 algorithm = "rprop+",
                 act.fct = "logistic",
                 linear.output = FALSE)

plot(fit)

without.fat <- scale.bodyfat
without.fat$waistcirc <- NULL
without.fat$hipcirc <- NULL

pred <- compute(fit, without.fat[-train,])
pred$net.result

fw <- waistcirc ~ DEXfat + age + elbowbreadth + kneebreadth +
  anthro3a + anthro3b + anthro3c + anthro4
fh <- hipcirc ~ DEXfat + age + elbowbreadth + kneebreadth +
  anthro3a + anthro3b + anthro3c + anthro4

regw <- lm(fw, data = scale.bodyfat[train,])
regh <- lm(fh, data = scale.bodyfat[train,])

predw <- predict(regw, without.fat[-train,])
predh <- predict(regh, without.fat[-train,])

mse(scale.bodyfat[-train, 10], pred$net.result[,1])  # using the neural network
mse(scale.bodyfat[-train, 10], predw)  # using the linear regression

mse(scale.bodyfat[-train, 10], pred$net.result[,2])  # using the neural network
mse(scale.bodyfat[-train, 10], predh)  # using the linear regression

X = as.matrix(without.fat[train,])
Y = as.matrix(scale.bodyfat[train,3:4])

fitB <- nn.train(x = X, y = Y,
                 initW = NULL,
                 initB = NULL,
                 hidden = c(8,4),
                 activationfun = "sigm",
                 learningrate = 0.02,
                 momentum = 0.74,
                 learningrate_scale = 1,
                 output = "linear",
                 numepochs = 970,
                 batchsize = 60,
                 hidden_dropout = 0,
                 visible_dropout = 0)

Xtest <- as.matrix(without.fat[-train,])
predB <- nn.predict(fitB, Xtest)

mse(scale.bodyfat[-train, 10], predB[,1])  # using the neural network
mse(scale.bodyfat[-train, 10], predB[,2])  # using the neural network