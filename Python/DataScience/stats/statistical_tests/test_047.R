# male: 18 out of 30
# female: 17 out of 24
tier_1_or_2 <- c(18, 17)
total <- c(30, 24)

# p-value = 0.5881 > 0.05 => don't reject null hypothesis that
# proportions are same therefore, no significant difference
# between the two groups
prop.test(tier_1_or_2, total, alternative = "two.sided", conf.level = 0.95)
