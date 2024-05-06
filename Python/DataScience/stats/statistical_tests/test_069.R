library(psych)

head(EuStockMarkets)

head(diff(EuStockMarkets, 1))

# Calculate the daily difference in the stock markets
d <- diff(EuStockMarkets, 1)

# p-value = 0 < 0.05 => reject null hypothesis of multivariate normality
# use 'small sample p-value' if 30 or fewer observations
mardia(x = d)
