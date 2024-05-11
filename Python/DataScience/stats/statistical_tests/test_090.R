library(urca)

# p-value < 0.05 => reject null hypothesis
summary(ur.sp(sunspots, type = "tau", pol.deg = 1, signif = 0.05))
