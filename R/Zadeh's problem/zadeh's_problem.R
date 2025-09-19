# Zadeh's problem:
#
# 2 experts are consulted about a patient
# There are 3 classes:
# - M = Meningitis
# - C = Concussion
# - T = Brain tumour
#
# Expert 1: 99% M, 1% C
# Expert 2: 99% T, 1% C
#
# e_i = hypothesis that the i(th) expert makes an error
# e_i_bar = hypothesis that the i(th) expert doesn't make an error
#
# Each expert is in error with probability p_ei = p_e
# If an expert is in error, the classification probabilities are uniform
# across all classes

# ------------------------------------------------------------------------------
# Naive Bayesian approach -- assume both experts are correct
# ------------------------------------------------------------------------------

joint <- function(x) {
    prior <- list(M=1/3, T=1/3, C=1/3)
    p_x <- prior[[x]]

    # Experts 1 and 2
    likelihoods_1 <- list(M=0.99, T=0, C=0.01)
    likelihoods_2 <- list(M=0, T=0.99, C=0.01)

    p_1 <- likelihoods_1[[x]]
    p_2 <- likelihoods_2[[x]]

    return(p_1 * p_2 * p_x)
}

joint_M = joint('M')
joint_T = joint('T')
joint_C = joint('C')

cat('Naive Bayesian approach:\n')
cat('p(M|Y) = ', joint_M / (joint_M + joint_T + joint_C), '\n')
cat('p(T|Y) = ', joint_T / (joint_M + joint_T + joint_C), '\n')
cat('p(C|Y) = ', joint_C / (joint_M + joint_T + joint_C), '\n')

# ------------------------------------------------------------------------------
# Multi-hypothesis approach
# ------------------------------------------------------------------------------

# Calculate p(x, y_1, y_2)
joint_with_error <- function(x, p_e) {
    prior <- list(M=1/3, T=1/3, C=1/3)
    likelihoods_error <- list(M=1/3, T=1/3, C=1/3)
    likelihoods_1 <- list(M=0.99, T=0, C=0.01)
    likelihoods_2 <- list(M=0, T=0.99, C=0.01)

    return(
        prior[[x]] *
         ((1-p_e)*likelihoods_1[[x]] + p_e*likelihoods_error[[x]]) *
         ((1-p_e)*likelihoods_2[[x]] + p_e*likelihoods_error[[x]])
    )
}

# Calculate p(x | y_1, y_2)
posterior <- function(x, p_e) {
    num = joint_with_error(x, p_e)
    den = joint_with_error('M', p_e) + joint_with_error('T', p_e) + joint_with_error('C', p_e)

    return(num/den)
}

# p(e_1, e_2 | y_1, y_2)
prob_error_given_state <- function(p_e, e_1, e_2) {
    p_e1 = p_e * e_1 + (1-p_e) * !e_1  # p(e_1)
    p_e2 = p_e * e_2 + (1-p_e) * !e_2  # p(e_2)

    prior <- list(M=1/3, T=1/3, C=1/3)
    likelihoods_error <- list(M=1/3, T=1/3, C=1/3)
    likelihoods_1 <- list(M=0.99, T=0, C=0.01)
    likelihoods_2 <- list(M=0, T=0.99, C=0.01)

    total = 0.0
    for (x in c('M', 'T', 'C')) {
        l1 = e_1 * likelihoods_error[[x]] + (!e_1) * likelihoods_1[[x]]
        l2 = e_2 * likelihoods_error[[x]] + (!e_2) * likelihoods_2[[x]]

        total = total + prior[[x]] * l1 * l2
    }

    num = p_e1 * p_e2 * total

    den = joint_with_error('M', p_e) + joint_with_error('T', p_e) + joint_with_error('C', p_e)

    return(num/den)
}

# Probability that an expert is in error
p_e = 0.01

cat('\nWith errors:\n')
cat('p(e) =', p_e, '\n')
cat('p(!e_1, !e_2) =', prob_error_given_state(p_e, FALSE, FALSE), '\n')
cat('p(!e_1, e_2) =', prob_error_given_state(p_e, FALSE, TRUE), '\n')
cat('p(e_1, !e_2) =', prob_error_given_state(p_e, TRUE, FALSE), '\n')
cat('p(e_1, e_2) =', prob_error_given_state(p_e, TRUE, TRUE), '\n')

cat('p(M|Y) =', posterior('M', p_e), '\n')
cat('p(T|Y) =', posterior('T', p_e), '\n')
cat('p(C|Y) =', posterior('C', p_e), '\n')
