# Coal mining disaster changepoint detection model
# http://people.math.aau.dk/~kkb/Undervisning/Bayes14/sorenh/docs/changepoint-notes.pdf

library(rjags)

D=c(4,5,4,1,0,4,3,4,0,6,
    3,3,4,0,2,6,3,3,5,4,5,3,1,4,4,1,5,5,3,4,2,5,2,2,3,4,
    2,1,3,2,1,1,1,1,1,3,0,0,1,0,1,1,0,0,3,1,0,3,2,2,0,1,
    1,1,0,1,0,1,0,0,0,2,1,0,0,0,1,1,0,2,2,3,1,1,2,1,1,1,
    1,2,4,2,0,0,0,1,4,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0)
yr=1851:1962
N=length(D)

plot(yr, D, xlab="Year", ylab = "Number of disasters, D")
lines(smooth.spline(yr,D), col='red')

# Count data => use a Poisson model
# Changepoint at some time c
# Different means before and after the changepoint

# Specify the model and save to a file
model.string <- "
model {
  
  # b[1] before changepoint, b[2] after
  for (j in 1:2) {
    b[j] ~ dnorm(0.0, 1.0E-6)  # small precision => large variance
  }

  for(year in 1:N) {
    log(mu[year]) <- b[1] + step(year - chg) * b[2]
    D[year] ~ dpois(mu[year])  # number of disasters
  }

  chg ~ dunif(1,N) # Uniform prior on the changepoint
}
"
writeLines(model.string, con = "temp_model.txt")

data = list(N=N,D=D)
inits = list(b=c(0,0),chg=40)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    inits = inits, n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("b", "chg"), n.iter = 1000)
plot(samples)
summary(samples)

stat <- summary(samples)$statistics
parm <- stat[,1]
yr <- 1:N
f1 <- exp( parm[1] + ((yr-parm[3])>0) * parm[2] )
plot(yr, D)
lines(yr, f1)
