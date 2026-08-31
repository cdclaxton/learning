#Bayesian #ML 

- "Bayesian analysis is the mathematics of re-allocating credability in a logically coherent and precise way" (J. K. Kruschke)
- Steps:
	- Define variables
	- Define the parameterised statistical model -- model desiderata:
		- Meaningful parameters
		- Descriptively adequate -- form should look like the data
	- Define prior distributions
	- Use Bayesian inference to reallocate credability
	- Perform a posterior predictive check
		- e.g. plot the model against the actual data
- The larger the sample size, the greater the precision (the smaller the variance) of the parameter estimates
- If the prior is broad and flat compared to the likelihood function, the prior will have little influence on the posterior
- Analysis can be conducted with different priors to assess their effects or priors can be combined (e.g. if experts disagree) into a joint prior thereby incorporating the uncertainty in the prior