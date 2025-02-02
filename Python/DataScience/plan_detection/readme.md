# Plan detection

## Introduction

This Python project explores an approach to performing plan detection using a principled, probabilistic approach.

Consider an entity that can be in one of a given number of defined states. The state in which the entity is in must be inferred from observations. An observation is in the form of an element from a set, as opposed to a continuous value with (x,y) coordinates. For simplicity, the time at which an observation is received can be assumed to have a discrete time step.

The observations do not uniquely define the state that the object is in, so for example an observation of type A could be associated with states 1 and 2.

The state of the entity evolves over time, but in such a way that the entity moves from state to state in a pre-defined sequence. There is no guarantee that the entity will be observed in each of the states as it progresses. Furthermore, the first observations of the entity may not correspond to the first state.

Observations are provided about the entity, but those observations are not under any control, so they arrive when generated by an external source. This means there isn't a continuous stream of observations as with a typical target tracking problem. Observations may not be transferred by the external system.

The problem is to estimate the state of the entity from the noisy and incomplete observations.

## One changepoint (two states)

Consider a situation where there are at most two states and there are four observations. With four observations there are three possible locations for a changepoint if it is assumed that the first observation has to belong to state 0. This illustrated below.

![](./two-states.png)

The probability of the observations $x$ given model 0 where there is just a single state 0 is given by:

$$
p(x | m_0) = \prod_{i=0}^{3} p(x_i | S_0).
$$

Model 1 has a single changepoint after observation $x_0$ and so its likelihood function is:

$$
p(x | m_1) = p(x_0 | S_0) \prod_{i=1}^{3} p(x_i | S_1).
$$

Model 2's changepoint occurs between $x_1$ and $x_2$ and so its likelihood function is:

$$
p(x | m_2) =  \prod_{i=0}^{1} p(x_i | S_0) \prod_{i=2}^{3} p(x_i | S_1).
$$

Finally, model 3 has a changepoint between $x_2$ and $x_3$:

$$
p(x | m_2) = \Big( \prod_{i=0}^{2} p(x_i | S_0) \Big) p(x_3 | S_1).
$$

The probability of the model given the observations is required, so Bayes' theorem needs to be employed. The posterior probability using Bayes' theorem is given by:

$$
p(m | x) = \frac{p(x | m)p(m)}{p(x)}
$$

The prior probability of each model $p(m)$ weights the likelihood of the observations given the model. Suppose that an analyst is able to provide the probability that there is one state or two states. Those two numbers would give $p(m_0)$ and $p(m_1) + p(m_2) + p(m_3)$ respectively. Models 1 to 3 require their own prior probability, but in the absence of domain knowledge, an uninformative prior in the form of a uniform distribution could be employed.

This experiment is coded in Python and can be found in `two_state_experiment.py`. The results of the changepoint model were compared to a model that randomly selects a sub-model using its prior probability.

### Experiment 1: No uncertainty in the observation to state mapping
Probability of only one state is 0.99 and the number of trials in the experiment is 1000. The CPT is:
| $ $ | $e_0$ | $e_1$ |
| -- | -- | -- |
| $S_0$ | $1$ | $0$ |
| $S_1$ | $0$ | $1$ |

The confusion matrix for the changepoint model (with an accuracy of 1.00000) is:
$$
\begin{bmatrix} 
0.9888 & 0.0 & 0.0 & 0.0 \\ 
0.0 & 0.0047 & 0.0 & 0.0 \\ 
0.0 & 0.0 & 0.0034 & 0.0 \\ 
0.0 & 0.0 & 0.0 & 0.0031 \\ 
\end{bmatrix}
$$

The confusion matrix for the random model (with an accuracy of 0.97940) is:
$$
\begin{bmatrix} 
0.9794 & 0.0033 & 0.0034 & 0.0027 \\ 
0.0047 & 0.0 & 0.0 & 0.0 \\ 
0.0034 & 0.0 & 0.0 & 0.0 \\ 
0.0031 & 0.0 & 0.0 & 0.0 \\ 
\end{bmatrix}
$$

### Experiment 2: Probability of 0.5 for each state, no uncertainty in the observation to state mapping
Probability of only one state is 0.5 and the number of trials in the experiment is 1000. The CPT is:
| $ $ | $e_0$ | $e_1$ |
| -- | -- | -- |
| $S_0$ | $1$ | $0$ |
| $S_1$ | $0$ | $1$ |

The confusion matrix for the changepoint model (with an accuracy of 1.00000) is:
$$
\begin{bmatrix} 
0.5142 & 0.0 & 0.0 & 0.0 \\ 
0.0 & 0.1608 & 0.0 & 0.0 \\ 
0.0 & 0.0 & 0.1617 & 0.0 \\ 
0.0 & 0.0 & 0.0 & 0.1633 \\ 
\end{bmatrix}
$$

The confusion matrix for the random model (with an accuracy of 0.33860) is:
$$
\begin{bmatrix} 
0.257 & 0.0833 & 0.0854 & 0.0885 \\ 
0.0773 & 0.027 & 0.0304 & 0.0261 \\ 
0.0793 & 0.0254 & 0.0277 & 0.0293 \\ 
0.0821 & 0.0262 & 0.0281 & 0.0269 \\ 
\end{bmatrix}
$$

### Experiment 3: Probability of 0.5 for each state
Probability of only one state is 0.5 and the number of trials in the experiment is 1000. The CPT is:
| $ $ | $e_0$ | $e_1$ |
| -- | -- | -- |
| $S_0$ | $0.9$ | $0.1$ |
| $S_1$ | $0.1$ | $0.9$ |

The confusion matrix for the changepoint model (with an accuracy of 0.83570) is:
$$
\begin{bmatrix} 
0.4513 & 0.0098 & 0.0045 & 0.0402 \\ 
0.003 & 0.1409 & 0.0115 & 0.0022 \\ 
0.0176 & 0.0161 & 0.1226 & 0.0147 \\ 
0.0163 & 0.0157 & 0.0127 & 0.1209 \\ 
\end{bmatrix}
$$

The confusion matrix for the random model (with an accuracy of 0.33640) is:
$$
\begin{bmatrix} 
0.2516 & 0.0828 & 0.0861 & 0.0853 \\ 
0.0769 & 0.0275 & 0.0273 & 0.0259 \\ 
0.089 & 0.0269 & 0.0282 & 0.0269 \\ 
0.0811 & 0.0273 & 0.0281 & 0.0291 \\ 
\end{bmatrix}
$$

### Analysis

Given how well an observation is a predictor of the state, an accuracy of 0.84 for Experiment 3 seems rather low. The problem is that there are technically two different models, one with just one stage and one with two stages. The more observations there are, the more places in which a changepoint can occur. The prior probability of any one changepoint configuration with two stages will decrease as the prior is essentially shared out equally. For example, if there were 100 observations, there are 99 locations for a changepoint and the prior of each possible changepoint location is divided by 99.

### Monte Carlo experiments

An experiment was performed with 10,000 trials with a random value of the probability of a single state (with values drawn from a uniform distribution in the range $[0,1]$) and a random CPT.

The confusion matrix for the changepoint model (with an accuracy of 0.64390) is:
$$
\begin{bmatrix} 
0.4521 & 0.0165 & 0.0123 & 0.0154 \\ 
0.0568 & 0.0757 & 0.0178 & 0.0178 \\ 
0.052 & 0.0361 & 0.0545 & 0.0252 \\ 
0.0641 & 0.0244 & 0.0177 & 0.0616 \\ 
\end{bmatrix}
$$

The confusion matrix for the max likelihood model (with an accuracy of 0.61110) is:
$$
\begin{bmatrix} 
0.3719 & 0.0418 & 0.0316 & 0.051 \\ 
0.0223 & 0.094 & 0.022 & 0.0298 \\ 
0.0237 & 0.046 & 0.063 & 0.0351 \\ 
0.0279 & 0.0343 & 0.0234 & 0.0822 \\ 
\end{bmatrix}
$$

The confusion matrix for the random model (with an accuracy of 0.44580) is:
$$
\begin{bmatrix} 
0.3326 & 0.0538 & 0.0588 & 0.0511 \\ 
0.0579 & 0.0386 & 0.036 & 0.0356 \\ 
0.0561 & 0.0379 & 0.0382 & 0.0356 \\ 
0.0573 & 0.036 & 0.0381 & 0.0364 \\ 
\end{bmatrix}
$$

The approach where all models are considered has the highest accuracy at 64 percent.

## Multiple changepoint detection algorithm approach

Suppose there are $L$ unique states numbered $0, 1, ..., L-1$. The states are assumed to be ordered by the progression that the entity follows, i.e. the entity exits state 0 into state 1 etc.

The ground truth time step at which a state transition occurs is denoted $\tau_l$. If there are $L$ states then there are $L-1$ change points.

There are $K$ observations of the entity numbered $0, 1, ..., K-1$. An observation $y_k$ is of a particular event type where there are $E$ event types (numbered $0, 1, ..., E-1$). An observation occurs at a time step $t_k$. An observation $x_i$ is given by the tuple

$$
x_i = (e_i, t_i), i \in [0, K-1]
$$

where $e_i$ is the observed event and $t_i$ is the time at which the observation was made.


If there was only a single state $S_0$, then the likelihood of the $K$ observations $e_k, k \in [0, K-1]$ is given by

$$
p(x | S_0) = \prod_{i=0}^{K-1} p(e_k | S_0)
$$

and thus the log-likelihood is given by

$$
\log p(x | S_0) = \sum_{k=0}^{K-1} \log p(e_k | S_0).
$$

Now suppose there are two states denoted $S_0$ and $S_1$. The time index at which the state transition occurs is denoted $\tau_0$. The likelihood of the observations

