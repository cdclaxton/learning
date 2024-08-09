library(urca)
library(tseries)

data(USeconomic)

m1 <- diff(USeconomic[, 1], 1)

plot(m1)

# Potential break at 76
# p-value < 0.05 => reject null hypothesis
summary(ur.za(m1, model = "both", lag = 3))
