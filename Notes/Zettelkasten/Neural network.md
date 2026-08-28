#ML 

**Hornik et al. theorem**: A continuous function $F$ on a bounded $n$-dimensional space can be approximated (to give $\hat{F}$) by a two-layer neural network with a finite number of hidden units such that $| F(x) - \hat{F}(x) < \epsilon|$.

Use more neurons per layer to detect finer structure in the data, however, the more hidden neurons, the greater the likelihood of overfitting (therefore, use as few as possible)

Classification task: Use the sign of the output to denote the class

