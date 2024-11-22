# Outlier detection

## Zero-inflated Poisson distribution

A zero-inflated Poisson distribution is essentially a mixture model of a process
that generates zeros and a second process that generates samples from a Poisson
distribution.

The probability of extra zeros is denoted $\pi$. The mean of the Poisson
distribution is denoted $\lambda$. It should be noted that both the zero 
generating process and the Poisson process contribute zeros.

The expected value of a ZIP distribution is given by:

$$
E(Y) = (1 - \pi) \lambda
$$

Consider the problem where there are two sets of data known to be derived from
ZIP distributions. The first set may represent some training data, such as
counts of events per day in a 90 day window. The second set may be a test set
looking at a shorter window of, say, 30 days. 

The problem is to determine the distribution over the ratio of the rates. This 
distribution may be used to calculate the probability that the ratio exceeds a 
threshold, e.g. that there is a 10 percent increase in events in the test 
window.

If independent estimators of $\pi$ and $\lambda$ are used for each of the two
datasets, then the ratio of the expected values is given by:

$$
r = \frac{E(Y_1)}{E(Y_2)} = \frac{(1 - \pi_1) \lambda_1}{(1 - \pi_2) \lambda_2}
$$

The Poisson hurdle model is an alternative formulation where $\pi$ represents 
the probability that a zero will occur. Instead of a Poisson distribution, a
truncated Poisson distribution is used instead.

$$
Pr(Y=y) = \begin{cases} 
          \pi & \text{if }y = 0 \\
          (1-\pi)\frac{\mu^y e^{-\mu}}{y!} & \text{if } y = 1,2,... \\
       \end{cases}
$$

The expected value of the Poisson hurdle model is given by:

$$
E(Y) = (1 - \pi) \frac{\mu}{1 - e^{-\mu}}
$$

## Zero-inflated negative binomial distribution

The expected value of the negative binomial distribution is given by

$$
E(Y) = \frac{r(1-p)}{p}
$$

and the variance by

$$
E(Y) = \frac{r(1-p)}{p^2}.
$$

The negative binomial distribution can be considered to be similar to a Poisson distribution, but with enlarged variance. Let the mean of the Poisson distribution be denoted $\lambda$. The increase in the variance compared to a Poisson distribution will be denoted $\delta$ where $\delta > 1$. Therefore,

$$
\lambda = \frac{r(1-p)}{p}
$$

and 

$$
\delta \lambda = \frac{r(1-p)}{p^2}.
$$

Rearranging the equation for the mean gives

$$
r = \frac{\lambda p}{1-p}
$$

and substituting this into the equation for the enlarged variance gives

$$
\delta \lambda = \frac{\lambda p}{1-p} \frac{1-p}{p^2} = \frac{\lambda}{p}.
$$

Therefore,

$$
p = \frac{1}{\delta}.
$$

From the equation for the mean

$$
\lambda = \frac{r(1-p)}{p} = \frac{r(1-\frac{1}{\delta})}{\frac{1}{\delta}} = r \delta (1 - \frac{1}{\delta}) = r (\delta - 1)
$$

Therefore,

$$
r = \frac{\lambda}{\delta - 1}.
$$
