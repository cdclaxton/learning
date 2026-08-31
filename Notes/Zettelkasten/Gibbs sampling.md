#ML #Bayesian 

- Typically applies to model with multiple parameters
- Special case of the [[Metropolis-Hastings algorithm]]
- At each point in the walk, one of the component parameters is selected (e.g. at random or cycled through in order)
	- Record values after a full cycle of parameters
- Generate a new value for $\theta_i$ from the conditional probability distribution $p(\theta_i|\{\ \theta_{j \neq i}\}, D)$
- Compard to the Metropolis algorithm:
	- Proposal move is always accepted (therefore, no inefficiency of rejected proposals)
	- No need to tune the proposal distribution
	- Must be able to derive the conditional distributions
	- Must be able to generate random samples from the conditional distributions
	- Progress can be stalled by highly correlated parameters