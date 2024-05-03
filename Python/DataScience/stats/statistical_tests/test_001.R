library(fBasics)
library(stats)

x <- c(44.4, 45.9, 41.9, 53.3, 44.7, 44.1, 50.7, 45.2, 60.1)
y <- c(2.6, 3.1, 2.5, 5.0, 3.6, 4.0, 5.2, 2.8, 3.8)

plot(x, y)

# p-value is 0.1082 => greater than the critical value of 0.05
# therefore don't reject the null hypothesis of zero correlation
cor.test(x, y, method = "pearson", alternative = "two.sided", conf.level = 0.95)

# p-value for all three alternative hypotheses
# all p-values are greater than 0.05, therefore don't reject the null hypothesis of zero correlation
# 95% confidence interval crosses zero, so don't reject the null hypothesis
correlationTest(x, y)
