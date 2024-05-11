library(circular)

sample <- split(swallows$heading, swallows$treatment)
sample

hist(sample$control)
hist(sample$shifted)

control <- circular(as.numeric(sample$control) * pi / 180)
treatment <- circular(as.numeric(sample$shifted) * pi / 180)

# P-value < 0.001 < 0.05 => reject null hypothesis
watson.two.test(control, treatment)
