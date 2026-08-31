# Bayesian estimation
#
# To run:
# Rscript beta_bernoulli.R

library(rjags)
source('DBDA2E-utilities.R')

# Define the data
N = 50  # Number of samples
z = 15  # Number of heads

y = c(rep(0,N-z), rep(1,z))

# Define the data for JAGS
dataList = list(
    y=y,
    N=N
)

# Specify the Bayesian model
modelString = "
model {
    for (i in 1:N) {
        y[i] ~ dbern(theta)  # Likelihood
    }
    theta ~ dbeta(1, 1)  # Prior
}
"

# Function to generate the chain initialisations
initsList = function() {
    resampledY = sample(y, replace=TRUE)
    thetaInit = sum(resampledY) / length(resampledY)  # Compute MLE
    thetaInit = 0.001 + 0.998*thetaInit  # Avoid 0 and 1
    return (
        list(theta=thetaInit)
    )
}

model <- jags.model(textConnection(modelString),
    data = dataList, inits=initsList, n.chains=3, n.adapt=500)

# Burn in
update(model, n.iter=500)

# Generate post-burn in samples
samples = coda.samples(model, variable.names=c('theta'), n.iter=5000)

diagMCMC(codaObject=samples, parName="theta",
    saveName='beta_bernoulli')

plotPost(samples[,"theta"], main="theta", xlab=bquote(theta),
    cenTend="median", compVal=0.5, ROPE=c(0.45, 0.55), credMass=0.90)