library(tseries)

data <- cumsum(rnorm(10000)) # contains a unit root

plot(data)

# p-value = 0.4004 > 0.05 => data contains a unit root
adf.test(data, alternative = "stationary")

# p-value = 0.5984
adf.test(data, alternative = "explosive", k = 10)
