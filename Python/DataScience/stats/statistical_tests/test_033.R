machine.1 <- c(10.8, 11.0, 10.4, 10.3, 11.3)
machine.2 <- c(10.8, 10.6, 11, 10.9, 10.7, 1.8)

# p-value = 0.0008893 < 0.05 => reject null hypothesis that the
# samples have the same variance
var.test(machine.1, machine.2,
    ratio = 1,
    alternative = "two.sided", conf.level = 0.95
)
