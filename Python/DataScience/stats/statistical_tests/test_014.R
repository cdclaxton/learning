library(UsingR)

x <- c(12, 2, 17, 25, 52, 8, 1, 12)

# Null hypothesis: sample median = 20
# p-value = 0.29 > 0.05 => don't reject null hypothesis that median = 20
simple.median.test(x, median = 20)
