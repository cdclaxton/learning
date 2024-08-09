library(psych)

# (x,y) Correlation between Stroop test and age: -0.2
# (x,z) Correlation between Full Scale measure and age: -0.28
# Age is a common variable
# (y,z) Correlation between Stroop test and Full Scale measure: 0.3
# (i.e. ignoring age)
# 123 participants

# p-value = 0.44 > 0.05 => don't reject the null hypothesis
res <- paired.r(xy = -0.2, xz = -0.28, yz = 0.30, 123, twotailed = TRUE)
res$t
res$p
