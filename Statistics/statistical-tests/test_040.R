library(lawstat)

count_data <- c(250, 260, 230, 270, 310, 330, 280, 360, 250, 230, 220, 260, 340, 270, 300, 320, 250, 240, 270, 290)
sample <- c("A", "A", "A", "A", "B", "B", "B", "B", "C", "C", "C", "C", "D", "D", "D", "D", "E", "E", "E", "E")

data <- data.frame((list(count = count_data, sample = sample)))

# p-value = 0.1416 > 0.05 => don't reject null hypothesis that the
# samples come from populations with equal variance
levene.test(data$count, data$sample,
    location = "median",
    correction.method = "zero.correction"
)
