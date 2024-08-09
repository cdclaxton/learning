library(psych)

# 187 participants
# Correlation between 'understanding from spouse' and wife's healthy dieting: -0.11
# Correlation between 'understanding from spouse' and husband's healthy dieting: 0.06
# Correlation between husband and wife's 'understanding from spouse': 0.41

# t-value = -2.15
# p-value < 0.033 < 0.05 => reject null hypothesis
r.test(187, r12 = -0.11, r34 = 0.06, r23 = 0.41)

# 2nd example:
# 103 observations
# F at time 1: index 1
# V at time 1: index 2
# F at time 2: index 3
# V at time 2: index 4

# z value = -1.4
# p-value > 0.16  > 0.05 => do not reject the null hypothesis
r.test(n = 103, r12 = 0.5, r13 = 0.7, r14 = 0.5, r23 = 0.5, r24 = 0.8, r34 = 0.6)
