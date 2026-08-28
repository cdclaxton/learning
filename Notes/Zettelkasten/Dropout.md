#ML 

Technique used in [[Neural network]]s

For each training case, each hidden neuron is randomly omitted from the network with a probability $p$, therefore different combinations of neurons may be used for each training instance

Results in weak learning at each epoch

Similar to concept of **bagging** (use the majority vote of multiple classifiers)

**Co-adaptation** -- 2+ neurons begin to detect the same feature repeatedly (similar to collinearity in linear regression)

Dropout discourages co-adaptation