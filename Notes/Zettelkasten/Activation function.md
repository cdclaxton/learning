#ML 

- Needed to introduce non-linearity to the neural network
- Limits the output of a neuron, e.g. in the range $[0,1]$ or $[-1,1]$
- For the backpropagation algorithm, the activation function must be differentiable

Popular functions:
- Sigmoid: $f(u) = \frac{1}{1 + \exp^{-cu}}$ where $f(u) \in [0,1]$
- Linear: $f(u) = u$
- Hyperbolic tangent: $f(u) = \tanh(cu)$ where $f(u) \in [-1,1]$
- Rectified linear unit (ReLU): $f(u) = \max(0,u)$
- Smooth (differentiable) approximation to ReLU: $f(u) = \log (1 + \exp(u))$

Softmax is common on the output layer to give a probability distribution over $k$ classes:

$$
f(u) = \frac{\exp(\frac{u}{T})}{\sum_k \exp(\frac{u}{T})}
$$

where $T$ is the temperature