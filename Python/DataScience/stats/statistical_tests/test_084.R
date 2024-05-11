DAX <- diff(EuStockMarkets[, 1], 1)
plot(DAX)

# p-value = 0.3944 > 0.05 => don't reject null hypothesis that
# the mean is zero
tseries::white.test(DAX)

CAC <- diff(EuStockMarkets[, 3], 1)
plot(CAC)

# p-value = 0.02109 < 0.05 => reject the null hypothesis
tseries::white.test(CAC)
