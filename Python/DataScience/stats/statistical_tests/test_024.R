x <- c(0.795, .864, .841, .683, .777, .720)
y <- c(.765, .735, 1.003, .778, .647, .740, .612)

# p-value = 0.4452 > 0.05 => don't reject null hypothesis that there is
# no difference
wilcox.test(x, y, alternative = "two.sided")
