library(tseries)

head(EuStockMarkets)

# p-value < 0.05 => reject null hypothesis
po.test(diff(log(EuStockMarkets), 1), demean = TRUE)
