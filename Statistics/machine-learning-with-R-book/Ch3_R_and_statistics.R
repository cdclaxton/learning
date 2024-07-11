# Chapter 3: R and Statistics
# ------------------------------------------------------------------------------

# Setup
setwd("C:/Users/cdc/OneDrive/Technical/Learning/R/MachineLearningWithR")

# Descriptive statistics -- summarise the characteristics of the data
# Inferential statistics -- infer characteristics of the population
#  (e.g. hypothesis testing, data estimation, data correlation)

## Understanding data sampling in R

# Randomly sample from a given population (with replacement)
sample(1:10, size = 5, replace = TRUE)
sample.int(10, size = 5)

## Operating probability distributions in R

# Plot the normal distribution
curve(dnorm(x, mean = 2, sd = 3), -10, 10)  # density
curve(pnorm(x, mean = 2, sd = 3), -10, 10)  # cumulative distribution
curve(pnorm(x, mean = 2, sd = 3, lower.tail = FALSE), -10, 10)
curve(qnorm(x, mean = 2, sd = 3), 0, 1) 

# Show a histogram of random samples from the normal distribution
hist(rnorm(100, mean = 2, sd = 3), xlim = c(-10,10))

# Show a histogram of samples from a uniform distribution
hist(runif(100, 0, 4), xlim = c(-1,5))

# Shapiro-Wilks test -- normality test
x <- rnorm(100, mean = 2, sd = 3)
shapiro.test(x)  # p-value is high, can't reject the null hypothesis (is Gaussian)

y <- runif(100, 0, 4)
shapiro.test(y)  # p-value is very low, can reject the null hypothesis

## Working with univariate descriptive statistics in R

# Univariate -- single variable for unit analysis
data("mtcars")
range(mtcars$mpg)
length(mtcars$mpg)
mean(mtcars$mpg)
median(mtcars$mpg)
sd(mtcars$mpg)
var(mtcars$mpg)
IQR(mtcars$mpg)  # Interquartile Rangle (IQR)
quantile(mtcars$mpg, 0.67)
max(mtcars$mpg)
min(mtcars$mpg)
cummax(mtcars$mpg)  # cumulative maximum
cummin(mtcars$mpg)  # cumulative minimum
summary(mtcars$mpg)
table(mtcars$cyl)  # frequency count

# Stem-and-leaf plot (frequency count of numerical data)
stem(mtcars$mpg)

# Histogram
library(ggplot2)
qplot(mtcars$mpg, binwidth = 2)

# Function to find the mode
mode <- function(x) {
  temp <- table(x)
  names(temp[temp == max(temp)])
}

x <- c(1,2,3,3,3,4,4,5,5,5,6)
mode(x)

## Performing correlations and multivariate analysis

# Multivariate descriptive statistics -- analyse relationship of 2 or more variables
cov(mtcars[1:3])  # can't compare strength of relationship
cor(mtcars[1:3])

library(reshape2)
qplot(x = Var1, y = Var2,
      data = melt(cor(mtcars[1:3])), fill = value, geom = "tile")

## Operating linear regression and multivariate analysis

# To fit variables using a linear model
lmfit <- lm(mtcars$mpg ~ mtcars$cyl)

# Null hypothesis: coefficient is equal to zero (no effect)
# Low p-value => can reject the null hypothesis (thus coefficient does have effect)
summary(lmfit)

# Null hypothesis is rejected if the F-value is large
anova(lmfit)

plot(mtcars$mpg ~ mtcars$cyl)
abline(lmfit)

## Conducting an exact binomial test

library(stats)
binom.test(x = 92, n = 315, p = 1/6)  # low p-value, reject null, die is loaded

## Performing student's t-test

# Assumes differences between samples are normally distributed
# Works best when the two samples are normally distributed
# One-sample t-test -- test whether 2 means are significantly different
# Two-sample t-test -- test whether means of 2 independent groups are different

boxplot(mtcars$mpg, mtcars$mpg[mtcars$am == 0], ylab = "mpg",
        names = c("Overall", "Automatic"))
abline(h = mean(mtcars$mpg), lwd = 2, col = "red")
abline(h = mean(mtcars$mpg[mtcars$am == 0]), lwd = 2, col = "blue")

mpg.overall <- mean(mtcars$mpg)
manual <- mtcars$mpg[mtcars$am == 0]
mpg.manual <- mean(manual) 
t.test(manual, mu = mpg.overall)  # low p-value => reject null

auto <- mtcars$mpg[mtcars$am == 1]
t.test(mtcars$mpg ~ mtcars$am)  # low p-value => reject null (i.e. is diff)

## Performing the Kolmogorov-Smirnov Test

# One-sample KS test: used to compare samples with a reference distribution
# Two-sample KS test: compare cumlative distributions of two datasets

x <- rnorm(50)
ks.test(x, "pnorm")  # high p-value, can't reject null hypothesis
ks.test(x, "punif")  # very low p-value, reject null hypothesis

# Generate two vectors of samples from a uniform distribution
x <- runif(n = 20, min = 0, max = 20)
y <- runif(n = 20, min = 0, max = 20)

# Plot the ECDF (Empirical Cumulative Distribution Function)
plot(ecdf(x), do.points = FALSE, verticals = TRUE, xlim = c(0,20))
lines(ecdf(y), lty = 3, do.points = FALSE, verticals = TRUE)

# Two-sample KS test (null hypothesis: x and y are from the same distribution)
ks.test(x, y)  # high p-value, can't reject null hypothesis

x <- runif(n = 20, min = 0, max = 20)
y <- rnorm(n = 20, mean = 10, sd = 1)

plot(ecdf(x), do.points = FALSE, verticals = TRUE, xlim = c(0,20))
lines(ecdf(y), lty = 3, do.points = FALSE, verticals = TRUE)

ks.test(x, y)  # low p-value, reject null hypothesis

## Understanding the Wilcoxon Rank Sum and Signed Rank test

# Wilcoxon Rank Sum and Signed Rank test (Mann-Whitney-Wilcoxon U-test)
# non-parameteric test of the null hypothesis
# population distribution of 2 groups are identical (doesn't assume Gaussian)

boxplot(mtcars$mpg ~ mtcars$am, ylab = "mpg", names = c("automatic", "manual"))
wilcox.test(mpg ~ am, data = mtcars)  # low p-value, reject null hypothesis

## Working with Pearson's Chi-squared test

# Do the distributions of two categorical variables differ?
library(stats)
ftable <- table(mtcars$am, mtcars$gear)
mosaicplot(ftable, main = "Number of forward gears within automatic and manual cars",
           color = TRUE)
chisq.test(ftable)  # low p-value

## Conducting a one-way ANOVA

# Analysis of variance (ANOVA) investigates the relationship between categorical
# independent variables and continuous dependent variables.
# Are the means of several groups equal?
# One-way ANOVA: one categorical variable.
# Two-way ANOVA: two categorical variables.

boxplot(mtcars$mpg ~ factor(mtcars$gear), xlab = "gear", ylab = "mpg")

# One-way ANOVA
oneway.test(mtcars$mpg ~ factor(mtcars$gear))  # low p-value

mpg.gear.aov <- aov(mtcars$mpg ~ factor(mtcars$gear))
summary(mpg.gear.aov)
model.tables(mpg.gear.aov, "means")
posthoc <- TukeyHSD(mpg.gear.aov)
plot(posthoc)

# Two-way ANOVA
par(mfrow = c(1,2))
boxplot(mtcars$mpg ~ mtcars$gear, subset = (mtcars$am == 0),
        xlab = "gear", ylab = "mpg", main = "Automatic")
boxplot(mtcars$mpg ~ mtcars$gear, subset = (mtcars$am == 1),
        xlab = "gear", ylab = "mpg", main = "Manual")

interaction.plot(mtcars$gear, mtcars$am, mtcars$mpg,
                 type = "b", col = c(1:3), 
                 xlab = "Number of gears", ylab = "Mean Miles Per Gallon")

mpg.anova2 <- aov(mtcars$mpg ~ factor(mtcars$gear) * factor(mtcars$am))
summary(mpg.anova2)