#Bayesian 

- From [[Bayes theorem]], the probability of the model $m$ given the data $D$ is given by:
$$
p(m|D) = \frac{p(D|m) p(m)}{\sum_{m} p(D|m) p(m)}
$$
- Each model may have its own set of prior distributions and a likelihood function
- Can be very sensitive to the choice of priors within the models, even if they're vague
- Relative posterior probabilities (posterior odds):
$$
\frac{p(m=1|D)}{p(m=2|D)} = \frac{p(D|m=1) p(m=1)}{p(D|m=2) p(m=2)}
$$
- Bayes factor: $\frac{p(m=1|D)}{p(m=2|D)}$
- Prior odds: $\frac{p(m=1)}{p(m=2)}$
- Substantial evidence for model $m=1$ when $BF > 3$
- Substantial evidence for model $m=2$ when $BF < \frac{1}{3}$
- Naturally accounts for model complexity
	- A more complex model can overfit
	- Each model must have a prior distribution over its parameters and more complex models dilute their prior distributions over a larger parameter space