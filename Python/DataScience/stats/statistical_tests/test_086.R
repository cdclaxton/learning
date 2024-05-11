data <- cumsum(rnorm(10000)) # contains a unit root

# p-value = 0.6161 > 0.05 => don't reject null hypothesis
PP.test(data)
