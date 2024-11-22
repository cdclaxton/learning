table_data <- as.table(rbind(c(20, 30), c(30, 20)))
dimnames(table_data) <- list(gender = c("male", "female"), party = c("Labour", "Conservative"))
table_data

# p-value = 0.07134 > 0.05 => don't reject the null hypothesis
fisher.test(table_data, alternative = "two.sided", conf.level = 0.95)

## Extubation failure example
patient_data <- as.table(rbind(c(11, 3), c(51 - 11, 11 - 3)))
dimnames(patient_data) <- list(
    four_scores = c("less than 12", "greater or equal to 12"),
    extubation = c("success", "failure")
)
patient_data

# p-value = 0.6997
fisher.test(patient_data, alternative = "two.sided", conf.level = 0.95)
