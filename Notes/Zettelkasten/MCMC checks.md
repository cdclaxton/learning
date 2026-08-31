#Bayesian 

- Mechanisms can only indicate violations of representativeness, i.e. they can't guarantee representativeness
- **Trace plot** -- graph of a sampled parameter as a function of step (iteration).
	- Superimpose 2 or more chains to see if they overlap
	- Look at the overlap of the density plot for different chains
	- Indications of a lack of convergence:
		- Isolated chains
		- Chains that linger on a parameter value or change very slowly
- **Shrink factor** (Gelman-Rubin statistic) -- value = 1 for converged chains, value > 1 for ophaned or stuck chains.
	- Looks at the variance between chains relative to variance within a chain
- **Effective sample size**:
	- Autocorrelation function $ACF(k)$ for lag $k$
	- For an estimate of the 95% HDI, an ESS of 10,000 is recommended
	- Effective sample size (practical to stop when $ACF(k) < 0.05$)
$$
ESS  = \frac{N}{1 + 2 \sum_{k=1}^{\inf} ACF(k)}
$$
- **Monte Carlo Standard Error** (MCSE)
$$
MCSE = \frac{SD}{\sqrt{ESS}}
$$
	- Interpreted on the scale of the parameter