# Chapter 4: Understanding Regression Analysis
# install.packages('car')  # Companion to Applied Regression
# install.packages('lmtest')
# install.packages('rms')
# install.packages('mgcv')
# ------------------------------------------------------------------------------

# Setup
setwd("C:/Users/cdc/OneDrive/Technical/Learning/R/MachineLearningWithR")

# Regression: Supervised learning method
# Model and analyse the relationship between a dependent (response) variable
# and one or more independent (predictor) variables

## Fitting a linear regression model with lm

library(car)
data("Quartet")

# Draw a scatter plot of the x and y variables
plot(Quartet$x, Quartet$y1)
lmfit <- lm(y1 ~ x, Quartet)  # dependent ~ independent (response ~ terms)
abline(lmfit, col = "red")
lmfit

# Use lsfit for simple linear regression
plot(Quartet$x, Quartet$y1)
lmfit2 <- lsfit(Quartet$x, Quartet$y1)
abline(lmfit2, col = "red")

## Summarising linear model fits
summary(lmfit)

coefficients(lmfit)
confint(lmfit, level = 0.95)  # Confidence interval
fitted(lmfit)  # Extract model fitted values
residuals(lmfit)  # Extract model residuals
anova(lmfit)  # ANOVA
vcov(lmfit)  # Variance-covariance matrix
influence(lmfit)  # Diagnose the quality of the regression fit

## Using linear regression to predict unknown values

lmfit <- lm(y1 ~ x, Quartet)
newdata <- data.frame(x = c(3,6,15))
predict(lmfit, newdata, interval = "confidence", level = 0.95)
predict(lmfit, newdata, interval = "predict")  # prediction interval

## Generating a diagnostic plot of a fitted model

# Diagnostics: Methods to evaluate assumptions
# Residuals vs. Fitted -- vertical distance from point to regression line
# Normal of residuals (Q-Q) -- Are the residuals normally distributed?
# Scale-Location -- square-root of the standardised residuals
# Residuals vs. Leverage -- How much each data point influences the regression
par(mfrow = c(2,2))
plot(lmfit)

# Compute the Cook's distance of each point (find outliers)
plot(cooks.distance(lmfit))

## Fitting a polynomial regression model with lm

plot(Quartet$x, Quartet$y2)
lmfit <- lm(Quartet$y2 ~ poly(Quartet$x, 2))  # fit quadratic
lines(sort(Quartet$x), lmfit$fit[order(Quartet$x)], col = "red")

# Fit a quadratic of the form y = a + bx + cx^2
plot(Quartet$x, Quartet$y2)
lmfit <- lm(Quartet$y2 ~ I(Quartet$x) + I(Quartet$x^2))
lines(sort(Quartet$x), lmfit$fit[order(Quartet$x)], col = "red")

## Fitting a robust linear regression model with rlm

# An outlier will move the regression line away
# Can just remove outliers or use a robust linear regression method

library(MASS)
plot(Quartet$x, Quartet$y3)
rlmfit <- rlm(Quartet$y3 ~ Quartet$x)  # use robust method
abline(rlmfit, col = "red")
lmfit <- lm(Quartet$y3 ~ Quartet$x)  # use the normal method
abline(lmfit, col = "blue")

## Studying a case of linear regression on SLID data

# Survey of Labour and Income Dynamics (SLID)
str(SLID)

# Visualise the variable wages against others
par(mfrow = c(2,2))
plot(SLID$wages ~ SLID$language)
plot(SLID$wages ~ SLID$age)
plot(SLID$wages ~ SLID$education)
plot(SLID$wages ~ SLID$sex)

# Fit a linear model to the data
lmfit <- lm(wages ~ ., data = SLID)
summary(lmfit)

# Drop the language attribute and draw a diagnostic plot
lmfit <- lm(wages ~ age + sex + education, data = SLID)
summary(lmfit)
plot(lmfit)

# Take the log of the wages and replot the diagnostic plot
lmfit <- lm(log(wages) ~ age + sex + education, data = SLID)
plot(lmfit)

# Diagnose the multi-colinearity (predictor is highly correlated with others)
# of the regression model
vif(lmfit)
sqrt(vif(lmfit)) > 2

# Diagnose the heteroscedasticity of the regression model
library(lmtest)
bptest(lmfit)  # low p-value, reject null hypothesis of homoscedasticity

library(rms)
olsfit <- ols(log(wages) ~ age + sex + education, data = SLID, x = TRUE, y = TRUE)
robcov(olsfit)

## Applying the Gaussian model for generalised linear regression

# Fit a Generalised Linear regression Model (GLM) with a Gaussian model
# Same as just using 'lm' function
lmfit1 <- glm(wages ~ age + sex + education, data = SLID, family = gaussian)
summary(lmfit1)

## Applying the Poisson model for generalised linear regression

# Poisson error distribution model
data("warpbreaks")
head(warpbreaks)
rs1 <- glm(breaks ~ tension, data = warpbreaks, family = poisson)
summary(rs1)

## Applying the Binomial model for generalised linear regression

head(mtcars$vs)
lm1 <- glm(vs ~ hp + mpg + gear, data = mtcars, family = binomial)
summary(lm1)

## Fitting a generalised additive model to the data

# GAM: semiparametric extension of GLM 
# GLM assumes a linear relationship, GAM fits using local behaviour

library(mgcv)
library(MASS)
str(Boston)

# Fit the regression using GAM
fit <- gam(dis ~ s(nox), data = Boston)
summary(fit)

## Visualising a generalised additive model

plot(Boston$nox, Boston$dis, xlab = "Nitrogen oxide concentration",
     ylab = "Weighted mean of distances")
x <- seq(0, 1, length = 500)
y <- predict(fit, data.frame(nox = x))
lines(x, y, col = "red", lwd = 2)

plot(fit, shade = TRUE)

fit2 <- gam(medv ~ crim + zn + crim:zn, data = Boston)
vis.gam(fit2)

## Diagnosing a generalised additive model

gam.check(fit)