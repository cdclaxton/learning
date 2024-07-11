# Test of two proportions

Notes from 
"Bayesian Tests of Two Proportions: A Tutorial With R and JASP"
Tabea Hoffmann, Abe Hofman, Eric-Jan Wagenmakers
https://meth.psychopen.eu/index.php/meth/article/view/9263/9263.html

* Comparison of the agreement of two proportions (A/B test)
* Two groups to compare, e.g. a control group and an intervention group
* Data for each group is dichotomous, e.g. correct-incorrect, dead-alive, side effect-no side effect
* Observed sample difference in the proportions must be translated to the population, which requires statistical inference

## Independent Beta Estimation (IBE) approach

* Group A has $n_A$ observations with $y_A$ successes
* Group B has $n_B$ observations with $y_B$ successes
* Bayesian A/B testing model:

$$
y_A \sim \text{Binomial}(n_A, \theta_A) \\
y_B \sim \text{Binomial}(n_B, \theta_B)
$$

where

$$
\theta_A \sim \text{Beta}(\alpha_A, \beta_A) \\
\theta_B \sim \text{Beta}(\alpha_B, \beta_B)
$$

Using Bayes' rule:

$$
p(\theta_A | y_A, n_A) = \frac{p(\theta_A) p(y_A, n_A | \theta_A)}{p(y_A, n_A)} \\
p(\theta_B | y_B, n_B) = \frac{p(\theta_B) p(y_B, n_B | \theta_B)}{p(y_B, n_B)}
$$

* $p(\theta_A)$ and $p(\theta_B)$ are the prior distributions
* Interested in $\delta = \theta_A - \theta_B$
* Posterior distribution for $\theta_A$ is $\text{Beta}(\alpga_A + s_A, \beta_A + f_A) and similarly for $\theta_B$
* See `independent_beta_estimation.R`
* Conversion rate uplift:

$$
\frac{\theta_B - \theta_A}{\theta_A}
$$

* A priori equally likely thay the training has a positive or negative effect and the possibility that both groups have the same approach rate is deemed impossible
* Assumptions behind the IBE approach:
    * The two success probabilities are independent
    * Effect is always present (positive or negative) as the continuous prior assigns no mass to a point value such as $\delta = 0$

## Logit Transformation Testing (LTT) approach

* Accounts for the dependency between the success probabilities of the two groups

$$
y_A \sim \text{Binomial}(n_A, \theta_A) \\
y_B \sim \text{Binomial}(n_B, \theta_B) \\
\log \Big(  \frac{\theta_A}{1 - \theta_A}  \Big) = \gamma - \psi/2 \\
\log \Big(  \frac{\theta_B}{1 - \theta_B}  \Big) = \gamma + \psi/2 \\
\gamma \sim N(\mu_\gamma, \sigma_\gamma^2) \\
\psi \sim N(\mu_\psi, \sigma_\psi^2) \\
$$

* $\gamma$ is the mean log odds and 
* $\psi$ is the distance between the two groups
* Four hypotheses:
    * $H_0: \theta_A = \theta_B$ -- identical success probabilities
    * $H_1: \theta \neq \theta_B$ -- success probabilities are not identical
    * $H_+: \theta_B > \theta_A$
    * $H_-: \theta_A > \theta_B$
* By comparing the hypotheses, it can be determined:
    * If there is a difference in the success probabilities (using $H_1$ and $H_0$)
    * If group B has a higher success probability than group A or whether the probabilities are the same ($H_+$ and $H_0$)
    * If group A has a higher success probability than group B or whether the probabilities are the same ($H_-$ and $H_0$)
    * If group B has a higher success probability than group A or does group A have a higher success probability than group B ($H_+$ and $H_-$)
* To compare the models' predictive performance:

$$
\frac{p(H_1 | data)}{p(H_0 | data)} = \frac{p(H_1)}{p(H_0)} \times \frac{p(data | H_1)}{p(data | H_0)} \\
\text{Posterior odds} = \text{Prior odds} \times \text{Bayes factor}
$$

* Prior odds = plausibility of the hypotheses before seeing the data
* Posterior odds = plausibility of the hypotheses after taking data into account
* Bayes factor = evidence

