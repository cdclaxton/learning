library(urca)

x <- rnorm(7000)

# p-value: < 2.2e-16 < 0.05 => reject null hypothesis of a unit root
summary(ur.ers(x, type = "DF-GLS", model = "trend", lag.max = 4))
