# Markov Random Fields

Run the unit tests with `make test`.

## Brute-force probability maximisation

![Four factor model](./images/four_factor.png)

## Image denoising

Image denoising using a Markov Random Field is implemented in `example2.c`. To run:

```bash
make example2

# Run using ./example2 <h> <eta> <beta>
./example2 -0.3 1 1
```

The noise-free binary image is denoted $\mathbf{x}$ where $x_i \in \{0, 1\}$ and $i$ runs over all pixels, so $i = 0, 1, ..., D-1$. The observed noisy image is denoted $\mathbf{y}$. The goal is to recover the noise-free image $\mathbf{x}$ given the noisy image $\mathbf{y}$.

The MRF for image denoising is shown below. The shaded nodes $y_i$ denote the observations.

![MRF for image denoising](./images/denoising.png)

The joint distribution over $\mathbf{x}$ and $\mathbf{y}$ is given by

$$
p(\mathbf{x}, \mathbf{y}) = \frac{1}{Z} \exp\{-E(\mathbf{x}, \mathbf{y}) \}
$$

where $E(\mathbf{x}, \mathbf{y})$ is an energy function given by

$$
E(\mathbf{x}, \mathbf{y}) = h \sum_{i} (2 x_i - 1) + \beta \sum_{\{i,j\}} |x_i - x_j| + \eta \sum_{i} |x_i - y_i|
$$

where $\{i,j\}$ is the set of neighbouring pixels. To maximise the probability $p(\mathbf{x}, \mathbf{y})$, minimise the energy $E(\mathbf{x}, \mathbf{y})$. 

The energy term $h \sum_{i} (2 x_i - 1)$ biases the model towards pixel values of 0 or 1. Setting $h = -1$ biases the model towards all ones, where as setting $h = 1$ biases the model towards all zeros.

The term $\beta \sum_{\{i,j\}} |x_i - x_j|$ causes the energy to be lower when neighbouring pixels in the denoised image have the same value.

The term $\eta \sum_{i} |x_i - y_i|$ causes the energy to be lower when the noise-free and noisy image have the same pixel values.

The noise-free image $\mathbf{x}$ is found using the simple iterative method of *Iterated Conditional Modes* (ICM), which is a coordinate-wise gradient descent algorithm.

## Inference on a chain

The diagram below shows a chain composed of three variables, $x_0$, $x_1$ and $x_2$.

![Three factor chain model](./images/chain.png)

The joint distribution is given by

$$
p(\mathbf{x}) = \frac{1}{Z} \psi_{0,1}(x_0, x_1) \psi_{1,2}(x_1, x_2) 
$$

where $Z$ is a normalising constant. Each node $x_i$ represents a discrete variable with $K$ states. The potential function $\psi_{n-1,n}(x_{n-1}, x_n)$ comprises a $K \times K$ table. Therefore, the joint distribution has $2 K^2$ parameters.

Suppose that none of the nodes have been observed. The problem is to find the marginal distribution of each node.

Inference on a chain, as illustrated above, can be implemented using a naive brute-force approach or by message passing. The aforementioned two inference methods are implemented in `example3.c`, which can be built and run using:

```bash
make example3
```

For ease of indexing in the code, $K \in \{0, 1, 2, 3\}$, i.e. each variable has four possible states. The marginal distribution can be represented as $3 \times K$ matrix, where each row represents one of three variables $x_i$ and the columns represent the $K$ states.

### Brute-force approach

The naive approach evaluates the joint distribution, which produces a $K^N = K^3$ matrix for $\mathbf{x}$. The summations are then performed explicitly so that

$$
p(x_n) = \sum_{x_0} \ldots \sum_{x_{n-1}} \sum_{x_{n+1}} \sum_{x_{N-1}} p(\mathbf{x})
$$

Note how the summation $\sum_{x_{n}}$ isn't included. To illustrate the marginal distribution, suppose there are only two variabls and that the joint distribution is given by the table shown below. 

![Joint distribution](./images/joint_distribution.png)

The marginal distribution for $x_1$ is given by

$$
p(x_1 = 0) = \sum_{x_2} p(x_1 = 0, x_2) = 0.2 + 0.5 = 0.7
$$

$$
p(x_1 = 1) = \sum_{x_2} p(x_1 = 1, x_2) = 0.15 + 0.15 = 0.3
$$

As expected, the sum of the marginal distributions is one.

Similarly, for $x_2$:

$$
p(x_2 = 10) = \sum_{x_1} p(x_1, x_2 = 10) = 0.2 + 0.15 = 0.35
$$

$$
p(x_2 = 11) = \sum_{x_1} p(x_1, x_2 = 11) = 0.5 + 0.15 = 0.65
$$

### Message passing approach

The joint distribution is given by

$$
p(\mathbf{x}) = \frac{1}{Z} \psi_{0,1}(x_0, x_1) \psi_{1,2}(x_1, x_2) 
$$

The marginal probability of $x_0$ is given by

$$
\begin{align*}
p(x_0) &= \frac{1}{Z} \sum_{x_1} \sum_{x_2} \psi_{0,1}(x_0, x_1) \psi_{1,2}(x_1, x_2) \\
&= \frac{1}{Z} \sum_{x_1} \psi_{0,1}(x_0, x_1) \sum_{x_2} \psi_{1,2}(x_1, x_2).
\end{align*}
$$

Let 

$$
\color{magenta} \mu_\beta(x_1) = \sum_{x_2} \psi_{1,2}(x_1, x_2)
$$

and so

$$
p(x_0) = \frac{1}{Z} \sum_{x_1} \psi_{0,1}(x_0, x_1) \color{magenta} \mu_\beta(x_1)
$$

and let

$$
\color{violet} \mu_\beta(x_0) = \sum_{x_1} \psi_{0,1}(x_0, x_1) \mu_\beta(x_1)
$$

Therefore,

$$
p(x_0) = \frac{1}{Z} \color{violet} \mu_\beta(x_0).
$$

Jumping to $p(x_2)$ (the last variable), its marginal distribution is given by

$$
\begin{align*}
p(x_2) &= \frac{1}{Z} \sum_{x_0} \sum_{x_1} \psi_{0,1}(x_0, x_1) \psi_{1,2}(x_1, x_2) \\
&= \frac{1}{Z} \sum_{x_1}\psi_{1,2}(x_1, x_2) \sum_{x_0} \psi_{0,1}(x_0, x_1).
\end{align*}
$$

Note the reordering of the summations. Let

$$
\color{teal} \mu_\alpha(x_1) = \sum_{x_0} \psi_{0,1}(x_0, x_1)
$$

and so

$$
p(x_2) = \frac{1}{Z} \sum_{x_1}\psi_{1,2}(x_1, x_2) \color{teal} \mu_\alpha(x_1)
$$

Let

$$
\color{blue} \mu_\alpha(x_2) = \sum_{x_1}\psi_{1,2}(x_1, x_2) \color{teal} \mu_\alpha(x_1)
$$

and so

$$
p(x_2) = \frac{1}{Z} \color{blue} \mu_\alpha(x_2)
$$

The final marginal distribution to calculate is $p(x_1)$, which is given by

$$
\begin{align*}
p(x_1) &= \frac{1}{Z} \sum_{x_0} \sum_{x_2} \psi_{0,1}(x_0, x_1) \psi_{1,2}(x_1, x_2) \\
&= \frac{1}{Z} \sum_{x_0}\psi_{0,1}(x_0, x_1) \sum_{x_2} \psi_{1,2}(x_1, x_2) \\
&= \frac{1}{Z} \color{teal} \mu_\alpha(x_1) \color{magenta} \mu_\beta(x_1) 
\end{align*}
$$

The terms $\mu_\alpha(x_1)$, $\mu_\alpha(x_2)$, $\mu_\beta(x_1)$ and $\mu_\beta(x_2)$ are called messages. In the implementation, each message is represented as a $K$-dimensional vector (array). For example,

$$
\mu_\alpha(x_1) = [ \mu_\alpha(x1=0), \mu_\alpha(x1=1), \ldots, \mu_\alpha(x1=K-1)]
$$