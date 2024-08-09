x <- c(0.795, .864, .841, .683, .777, .720)
y <- c(.765, .735, 1.003, .778, .647, .740, .612)

# p-value = 0.67 > 0.05 => can't reject null hypothesis that means are equal
t.test(x, y, alternative = "two.sided", var.equal = TRUE)
