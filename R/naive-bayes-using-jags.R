# Naive Bayes model using JAGS

library(rjags)

# JAGS model
model_string <- "
model {
    c ~ dbern(p_c)
    f0 ~ dbern(cpt_f0[c + 1, 2])
    f1 ~ dbern(cpt_f1[c + 1, 2])
}
"

# Prior probability of the class c
p_c <- 0.6

# CPTs
#
#          f
#      | 0  1
#  ------------
#    0 | a  b
#  c 1 | c  d
#
p_f0_given_c_0 = 0.5
p_f0_given_c_1 = 0.8

p_f1_given_c_0 = 0.3
p_f1_given_c_1 = 0.6

cpt_f0 <- matrix(c(
    (1-p_f0_given_c_0), p_f0_given_c_0,
    (1-p_f0_given_c_1), p_f0_given_c_1
    ), nrow = 2, byrow = TRUE)

cpt_f1 <- matrix(c(
    (1-p_f1_given_c_0), p_f1_given_c_0,
    (1-p_f1_given_c_1), p_f1_given_c_1
    ), nrow = 2, byrow = TRUE)

f0 <- 1
f1 <- 1

# Calculate the expected posterior probability of the class
p_f = p_c * cpt_f0[2, f0 + 1] * cpt_f1[2, f1 + 1] +
     (1-p_c) * cpt_f0[1, f0 + 1] * cpt_f1[1, f1 + 1]
posterior <- p_c * cpt_f0[2, f0 + 1] * cpt_f1[2, f1 + 1] / p_f

model <- jags.model(textConnection(model_string),
    data = list(cpt_f0 = cpt_f0, cpt_f1 = cpt_f1, p_c = p_c, f0 = f0, f1 = f1))

update(model, n.iter = 10000, progress.bar = "none")

samples <- coda.samples(model,
    variable.names = c("c"),
    n.iter = 20000,
    progress.bar = "none")

# plot(samples)

mat <- as.matrix(samples)
cat("Mean of c:", mean(mat[, "c"]), "\n")
cat("Posterior probability p(c=1|f) =", posterior, "\n")