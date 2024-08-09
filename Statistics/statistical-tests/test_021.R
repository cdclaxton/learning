sample1 <- c(2.9, 3.5, 2.8, 2.6, 3.7, 4.0)
sample2 <- c(3.9, 2.5, 4.3, 2.7, 2.6, 3.0)
sample3 <- c(2.9, 2.4, 3.8, 1.2, 2.0, 1.97)

sample <- c(sample1, sample2, sample3)

g <- factor(rep(1:3, c(6, 6, 6)), labels = c("sample1", "sample2", "sample3"))

# Don't reject null hypothesis for all pairs of samples
# None of the differences in the mean are significantly different from zero
pairwise.t.test(sample, g,
    p.adjust.method = "holm", paired = TRUE,
    alternative = "two.sided"
)
