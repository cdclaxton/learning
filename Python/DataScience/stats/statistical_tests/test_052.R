# Does a drug have an effect on a particular disease?
# diagnosis: present or absent
# before and after treatment
data <- matrix(c(101, 59, 121, 33),
    nrow = 2,
    dimnames = list(
        "before" = c("present", "absent"),
        "after" = c("present", "absent")
    )
)
data

# p-value = 5.45e-06 < 0.05 => reject null hypothesis of no treatment effect
mcnemar.test(data)
