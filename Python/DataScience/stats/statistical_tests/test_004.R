library(psych)

# Correlation A: 0.54 (17 pairs)
# Correlation B: 0.89 (26 pairs)
# p-value = 0.01584569 < 0.05 => reject null hypothesis that there is no
# difference in the correlation coefficients
x <- paired.r(0.54, 0.89, NULL, 17, 26, twotailed = TRUE)
x$test
x$z
x$p
