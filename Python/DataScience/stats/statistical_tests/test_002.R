library(stats)

x <- c(44.4, 45.9, 41.9, 53.3, 44.7, 44.1, 50.7, 45.2, 60.1)
y <- c(2.6, 3.1, 2.5, 5.0, 3.6, 4.0, 5.2, 2.8, 3.8)

plot(x, y)

# Spearman rank correlation is 0.6
# p-value=0.0968 => don't reject the null hypothesis (zero correlation between variables)
cor.test(x, y, method = "spearman", alternative = "two.sided")
