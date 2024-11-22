library(survival)

time <- c(13, 18, 28, 26, 21, 22, 24, 25, 10, 13, 15, 16, 17, 19, 25, 32) # months
status <- c(1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1)
treatment.group <- c(1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2)
sex <- c(1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2) # 1 = male

# p-value > 0.05 => cannot reject null hypothesis that the survival times are
# similar between the two groups
survdiff(Surv(time, status) ~ treatment.group, rho = 0)
