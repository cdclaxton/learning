#Bayesian 

- Used to reduce autocorrelation in MCMC-based [[Bayesian inference]]
- Useful when two models are encoded and being computed simultaneously
- Helps the chain jump between models more efficiently
- Method:
	- Run initially with the pseudo priors set to the true priors
	- Note the marginal posteriors on the parameters
	- Set the pseudo priors to constants that match the marginal posteriors from the previous step
	- Re-run the Bayesian inference with the pseudo priors