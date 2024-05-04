# time in water: 1-3hrs, 4-6hrs, >6hrs
infected.swimmers <- c(5, 5, 33)
all.swimmers <- c(13, 8, 37)

# p-value = 0.000231  < 0.05 => reject the null hypothesis of no linear trend
# therefore attack rate highest for those spending more time in the water
prop.trend.test(infected.swimmers, all.swimmers)
