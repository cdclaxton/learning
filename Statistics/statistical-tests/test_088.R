library(tseries)

x <- rnorm(7000)

# p-value = 0.1
kpss.test(x, null = "Level")

# p-value = 0.1
kpss.test(x, null = "Trend")
