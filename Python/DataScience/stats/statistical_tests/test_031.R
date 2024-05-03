first_sample <- c(3.18, 3.28, 3.92, 3.6, 3.0, 3.45, 3.74)
second_sample <- c(3.55, 2.76, 2.13, 2.48, 3.67, 3.0)

# Make a dataframe
all_samples <- c(first_sample, second_sample)
sample_indexes <- factor(c(
    rep(0, length(first_sample)),
    rep(1, length(second_sample))
))

df <- data.frame(all_samples, sample_indexes)

# Order the dataframe by sample value
df <- df[order(df$all_samples), ]
df

# Run the test
# p-value = 0.7535 > 0.05 => don't reject null hypothesis of randomness
tseries::runs.test(df$sample_indexes)
