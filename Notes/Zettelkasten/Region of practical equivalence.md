#Bayesian 

- ROPE
- Small range of parameter values that are considered practically equivalent to the null value
- A parameter value is declared **not credible** (or rejected) if the **entire ROPE** lies outside the 95% HDI of the posterior distribution of the parameter
- A parameter value is accepted if that value's ROPE **completely contains** the 95% HDI of the posterior
- **Withhold a decision** when the HDI and ROPE overlap, but the ROPE is not completely contained in the HDI
- Can plot the proportion of the posterior that falls within the ROPE for different ROPE widths