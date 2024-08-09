DAX <- diff(EuStockMarkets[, 1], 1)
SMI <- diff(EuStockMarkets[, 2], 1)
CAC <- diff(EuStockMarkets[, 3], 1)
FTSE <- diff(EuStockMarkets[, 4], 1)

# p-value < 0.05 => reject the null hypothesis that the samples
# come from the same distribution
kSamples::ad.test(DAX, SMI, CAC, FTSE)
