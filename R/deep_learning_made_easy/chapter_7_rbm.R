library(deepnet)

# ------------------------------------------------------------
# Generate the data
# ------------------------------------------------------------

n_samples <- 10
p <- 0.7  # Probability of type 1

samples <- matrix(0, n_samples, 3)

for (i in 1:n_samples) {
	if (rbinom(1,1,p) == 1) {
		samples[i,] = c(1,0,1)
	} else {
		samples[i,] = c(0,1,0)
	}
}

# ------------------------------------------------------------
# Train a Restricted Boltzmann Machine
# ------------------------------------------------------------

rbm_model <- rbm.train(samples,
	hidden=1,
	numepochs=100,
	hidden_type="bin",
	visible_type="bin")

# ------------------------------------------------------------
# Generate samples
# ------------------------------------------------------------

# 1. Initialize a random seed vector
num_samples <- 5
n_features <- 3
generated_samples <- matrix(round(runif(num_samples * n_features)), 
                            nrow = num_samples, 
                            ncol = n_features)

# 2. Run Gibbs sampling iterations to let the model generate data
# Higher iterations generally lead to samples closer to the true model distribution
gibbs_steps <- 50

for (i in 1:gibbs_steps) {
  # Step A: Move from visible to hidden units
  hidden_activations <- rbm.up(rbm_model, generated_samples)
  
  # Step B: Move back from hidden to visible units
  generated_samples <- rbm.down(rbm_model, hidden_activations)
}

# Convert probabilities to binary values
recon <- ifelse(generated_samples >= 0.5, 1, 0)

print(recon)