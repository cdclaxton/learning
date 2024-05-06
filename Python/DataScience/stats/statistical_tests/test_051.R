data <- array(c(12, 16, 7, 19, 16, 11, 5, 20),
    dim = c(2, 2, 2),
    dimnames = list(
        Treatment = c("Drug", "Placebo"),
        Response = c("Improved", "No change"),
        Sex = c("Male", "Female")
    )
)
data

# p-value = 0.003953 < 0.05 => reject null hypothesis
mantelhaen.test(data,
    alternative = "two.sided",
    correct = FALSE, exact = FALSE, conf.level = 0.95
)
