#ML 

- Unsupervised three-layer feedforward [[Neural network]]
- Input and output layers have the same number of nodes
- Trained to reconstruct its own input by learning the identity function
- Consists of:
	- **Encoder** -- input layer to hidden layer
	- **Decoder** -- hidden layer to output layer
- Hidden layer can be considered as a feature representation of the input
	- More hidden layers than inputs => maps the input to a higher dimensional space
	- Fewer hidden layers => compresses the input attributes (requires the input attributes to be correlated)
- Can be used as a **feature extractor** by using the output of the hidden layer
- Use for anomaly detection by looking for outliers in the reconstruction error

**Sparse autoencoder**:
- Large number of hidden neurons
- Only a small fraction of the hidden neurons are active
- Training involves a sparsity constraint