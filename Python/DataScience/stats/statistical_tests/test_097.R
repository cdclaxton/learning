library(circular)

ants <- as.numeric(fisherB10[[1]])
ants

ants_radians <- ants * pi / 180

# p-value < 0.05 => reject null hypothesis of uniformity
rayleigh.test(ants_radians)
