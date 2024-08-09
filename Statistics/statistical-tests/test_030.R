# Generate independent and identically distributed data
set.seed(1234)
x <- rnorm(1000)

plot(x)

# All p-values are > 0.05 => can't reject null hypothesis of IID data
tseries::bds.test(x, m = 6)

# Daily closing DAX stock market index (1991 - 1998)
plot(EuStockMarkets[, 1])

diff_DAX <- diff(EuStockMarkets[, 1], 1)
plot(diff_DAX)

# All p-values are reported as zero => strongly reject the null hypothesis
# that the daily difference is IID
tseries::bds.test(diff_DAX, m = 6)
