count_data <- c(250, 260, 230, 270, 310, 330, 280, 360, 250, 230, 220, 260, 340, 270, 300, 320, 250, 240, 270, 290)
sample <- c("A", "A", "A", "A", "B", "B", "B", "B", "C", "C", "C", "C", "D", "D", "D", "D", "E", "E", "E", "E")

# p-value = 0.5886 > 0.05 => don't reject the null hypothesis
car::leveneTest(count_data, factor(sample))
