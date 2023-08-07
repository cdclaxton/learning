# Multi-hypothesis approach to combining discrete probability distributions

Consider a set of hypotheses where each hypotheis has an associated prior probability of being true and a discrete probability distribution representing an effect if the hypothesis is true.

Each hypothesis is in the form of a set of variables that are either true or false. For example, the hypothesis $H_1$ is represented as $A.\bar{B}$ where variable $A$ is true and $B$ is false.

The `Hypotheses` struct represents the hypotheses, with each hypothesis having a prior probability and an associated probability distribution. Calling the `Evaluate()` method with the probability that each variable is true returns the overall probability distribution.
