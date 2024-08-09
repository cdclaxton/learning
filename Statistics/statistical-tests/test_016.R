sample1 <- c(2.9, 3.5, 2.8, 2.6, 3.7)
sample2 <- c(3.9, 2.5, 4.3, 2.7)
sample3 <- c(2.9, 2.4, 3.8, 1.2, 2.0)

sample <- c(sample1, sample2, sample3)

g <- factor(rep(1:3, c(5, 4, 5)), labels = c("sample1", "sample2", "sample3"))

# None of the p-values suggest the null hypothesis can be rejected
pairwise.t.test(sample, g,
    p.adjust.method = "holm", pool.sd = FALSE,
    alternative = "two.sided"
)
