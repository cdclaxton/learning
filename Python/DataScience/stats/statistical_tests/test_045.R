sample <- rbind(
    s1 = c(95, 106), s2 = c(181, 137), s3 = c(76, 85),
    s4 = c(13, 29), s5 = c(11, 26), s6 = c(201, 179)
)
colnames(sample) <- c("treat1", "treat2")
sample

# Using Holm adjustment: s2-s4 and s2-s5 are significant at 5% level
pairwise.prop.test(sample, p.adjust.method = "holm")

# Using Benjamini and Yekutieli adjustment: no pairs significant at 5% level
# BY is more conservative
pairwise.prop.test(sample, p.adjust.method = "BY")

smokers <- c(83, 90, 129, 70)
patients <- c(86, 93, 136, 82)
pairwise.prop.test(smokers, patients)
