# Two-to-one mapping

Suppose there are $N > 0$ pairs of values $(x_i, y_i)$ where $x_i \in [0, x_{max}]$ and $y_i \in [0, y_{max}]$. The upper bounds on the range are such that $x_{max} \ge 0$ and $y_{max} \ge 0$.

The pairs $(x_i, y_i)$ can be represented as two vectors denoted $\bold{x}$ and $\bold{y}$ where each vector is of length $N$.

The problem is to find a mapping of the two vectors $\bold{x}$ and $\bold{y}$ to a single vector $\bold{d}$ such that:

* The result $d_i$ where $i \in [0, N-1]$ is a single number in the range $[-1, 1]$.
* If $x_{max}$ and $y_{max}$ are significantly different that the result is not dominated by one or the other.
* The centre point, denoted by a result of $d_i = 0$, is reserved for cases where $x_i = y_i = 0$.

## Normalised opposites approach

The values of $\bold{x}$ can be normalised in the range $[0,1]$ by scaling the values using:

$$
\bold{x}' = \frac{1}{x_{max}} \bold{x}
$$

where $x_{max} = \max(\bold{x})$ if $\max(\bold{x}) > 0$, else $x_{max} = 1$ if $\max(\bold{x}) =0$. This prevents division by 0.

Similarly, $\bold{y}$ can be normalised using:

$$
\bold{y}' = \frac{1}{y_{max}} \bold{y}.
$$

The difference between the two normalised values $d$ can be found from:

$$
\bold{d} = \frac{1}{x_{max}} \bold{x} - \frac{1}{y_{max}} \bold{y}
$$

The value of $\bold{d}$ will be in the range $[-1,1]$. To ensure an element of $d$ reaches the one or other bounds if there is a value of $d_i > 0$:

$$
\bold{d}' = \frac{1}{\alpha} \Big( \frac{1}{x_{max}} \bold{x} - \frac{1}{y_{max}} \bold{y} \Big)
$$

where $\alpha = \max(|\bold{d}|)$ where $|\bold{d}|$ represents the absolute value of each element in the vector.