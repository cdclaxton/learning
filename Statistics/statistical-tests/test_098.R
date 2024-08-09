library(circular)

ants <- as.numeric(fisherB10[[1]])
ants

ants_radians <- ants * pi / 180

# p-value > 0.05 => can't reject null hypothesis that data is
# from the Von Mises distribution
watson.test(ants_radians, dist = "vonmises")

# P-value < 0.01 => reject null hypothesis that data is from
# a uniform distribution
watson.test(ants_radians, dist = "uniform")
