library(outliers)

count_data <- c(250, 260, 230, 270, 310, 330, 280, 360, 250, 230, 220, 260, 340, 270, 300, 320, 250, 240, 270, 290)
sample <- c("A", "A", "A", "A", "B", "B", "B", "B", "C", "C", "C", "C", "D", "D", "D", "D", "E", "E", "E", "E")

data <- data.frame((list(count = count_data, sample = sample)))

# Function identifies that group B has the largest variance
# p-value = 0.67 > 0.05 => don't reject null hypothesis of equal variances
cochran.test(count ~ sample, data, inlying = FALSE)

# Test for smallest variance
# Function identifies that group A has the lowest variance
# p-value < 0.05 => reject null hypothesis of equality of variances
cochran.test(count ~ sample, data, inlying = TRUE)
