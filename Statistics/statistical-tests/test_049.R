table_data <- as.table(rbind(c(20, 30), c(30, 20)))
table_data

dimnames(table_data) <- list(
    gender = c("male", "female"),
    party = c("Labour", "Conservative")
)
table_data

# without continuity correction
# p-value < 0.05 => reject null hypothesis
chisq.test(table_data, correct = FALSE)

# with continuity correction (for a small number of observations)
# p-value > 0.05 => DON'T reject null hypothesis
chisq.test(table_data, correct = TRUE)
