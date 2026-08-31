#ML #Bayesian 

- Examples:
	- [[Metropolis algorithm]]
	- [[Gibbs sampling]]
- [[MCMC checks]]
- **Burn-in period** -- to remove unrepresentative initial values before a chain reaches the modal region of the posterior
- To improve the efficiency of MCMC:
	- Run chains in parallel
	- Adjust the sampling method -- e.g. use Gibbs sampling over a Metropolis sampler (or Hamiltonian Monte Carlo)
	- Change the parameterisation of the model
- **Thinning** -- reduce autocorrelation in a chain
	- Keep only the $k^{th}$ step in the chain
	- Useful for reducing memory consumption
	- Thinned chain has less information that the original chain
	- Estimates from the thinned chain are (on average) less stable and accurate than from the original chain