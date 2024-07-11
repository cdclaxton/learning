# Chapter 1: Practical machine learning with R
# ------------------------------------------------------------------------------

## Reading and writing data

# Setup
setwd("C:/Users/cdc/OneDrive/Technical/Learning/R/MachineLearningWithR")

# To view the built-in datasets
data()

# Load the Iris dataset
data(iris)

# View the data type
class(iris)

# Save the object data to a file
save(iris, file = "myData.RData")

# Load the data
load("myData.RData")

# Import text data into a data frame
test.data <- read.table(file = "./data/simple_file.txt", header = TRUE)

# Export data to a text file
write.table(test.data, file = "./data/simple_file_write.txt", sep = ",")

# Export as CSV
write.csv(test.data, file = "./data/simple_file_write.csv")

# Read a CSV file
csv.data <- read.csv("./data/simple_file_write.csv", header = TRUE, row.names = 1)

## Using R to manipulate data

data(iris)

# Select a field from the first row
iris[1, "Sepal.Length"]

# Select multiple columns
iris[, c("Sepal.Length", "Sepal.Width")]

# Summarise and display the internal structure
str(iris)

# Subset by row and column
iris[1:5, c("Sepal.Length", "Sepal.Width")]

# Subset by condition
iris[iris$Species == "setosa", ]

# Get indices of satisfied data
which(iris$Species == "setosa")

# Subset
subset(iris, Petal.Length <= 1.4 & Petal.Width >= 0.2, select = Species)

# Merge data
flower.type <- data.frame(Species = "setosa", Flower = "iris")
merge(flower.type, iris[1:3,], by = "Species")

# Order data
head(iris[order(iris$Sepal.Length, decreasing = TRUE), ])

## Applying basic statistics
mean(iris$Sepal.Length)
sd(iris$Sepal.Length)
var(iris$Sepal.Length)
min(iris$Sepal.Length)
max(iris$Sepal.Length)
median(iris$Sepal.Length)
range(iris$Sepal.Length)
quantile(iris$Sepal.Length)

# Find the mean of the numeric variables (ignoring NA values)
sapply(iris[1:4], mean, na.rm = TRUE)

# Get a summary
summary(iris)

# Correlation
cor(iris[,1:4])

# Covariance
cov(iris[,1:4])

# Perform a t-test
s <- iris$Petal.Width[iris$Species == "setosa"]
v <- iris$Sepal.Width[iris$Species == "versicolor"]
t.test(s, v)

# Perform a correlation test
cor.test(iris$Sepal.Length, iris$Sepal.Width)

# Use of aggregate to calculate summary statistics
aggregate(x = iris[,1:4], by = list(iris$Species), FUN = mean)

## Visualising data

# Calculate frequency of species
table(iris$Species)

# Draw a pie chart
pie(table(iris$Species))

# Draw a histogram
hist(iris$Sepal.Length)

# Draw a box and whisker plot
# line represents the median
# box represents the upper and lower quantiles
boxplot(Petal.Width ~ Species, data = iris)

# Scatter plot
plot(x = iris$Petal.Length, iris$Petal.Width, col = iris$Species)

# Generate scatter plots of pairs
pairs(iris[1:4], main = "Edgar Anderson's Iris Data", pch = 21, 
      bg = c("red", "green3", "blue")[unclass(iris$Species)])

## Getting a dataset for machine learning

# UCI machine learning repository
# http://archive.ics.uci.edu/ml/

# Read the 'flags' dataset
u <- "http://archive.ics.uci.edu/ml/machine-learning-databases/flags/flag.data"
colnames <- "name,landmass,zone,area,population,language,religion,bars,stripes,colours,red,green,blue,gold,white,black,orange,mainhue,circles,crosses,saltires,quarters,sunstars,crescent,triangle,icon,animate,text,topleft,botright"
colnames <- unlist(strsplit(colnames, split=","))
flags <- read.csv(url(u), header = FALSE, col.names = colnames)
