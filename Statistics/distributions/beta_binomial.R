# Beta-binomial model
# http://www4.stat.ncsu.edu/~reich/st590/code/BetaBinomJAGS

library(rjags)

n <- 20
Y <- 4
a <- 3
b <- 1

model_string <- "
model{
  # Likelihood
  Y ~ dbinom(theta,n)
  
  # Prior
  theta ~ dbeta(a, b)
}"

model <- jags.model(textConnection(model_string), 
                    data = list(Y=Y,n=n,a=a,b=b))

update(model, 10000, progress.bar="none"); # Burnin for 10000 samples

samp <- coda.samples(model, 
                     variable.names=c("theta"), 
                     n.iter=20000, progress.bar="none")

summary(samp)

plot(samp)

