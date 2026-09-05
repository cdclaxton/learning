#Bayesian 

- Should a particular value of a parameter be rejected?
- **p-value** -- probability of getting an outcome from the null hypothesis that is as or more extreme than the actual outcome
- Reject the null hypothesis if the p-value is less than, say, 5%
- Depends upon the space of all possible outcomes
- Decision rule causes us to reject the null hypothesis 5% of the time when the null hypothesis is true
- We don't accept the null hypothesis, we fail to reject it
- Key flaw: Different p-values for different stopping intentions, e.g. the number of flips of a coin, the number of flips required to get $z$ heads or the number of flips in a given duration
- Does not take into account prior knowledge, unlike [[Bayesian inference]]
- NHST only tells us whether the value is extreme, as opposed to the Bayesian posterior which gives credabilities
- The null hypothesis will always be rejected (even if it is true) when doing sequential testing without time constraints (keep checking the result until $p < 0.05$)
- 