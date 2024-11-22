library(PairedData)

machine.am <- c(10.8, 11.0, 10.4, 10.3, 11.3, 10.2, 11.1)
machine.pm <- c(10.8, 10.6, 11, 10.9, 10.9, 10.7, 1.8)

# p-value = 0.0002258 => reject null hypothesis that variances are equal
pitman.morgan.test.default(machine.am, machine.pm, ratio = 1, conf.level = 0.95)
