# Simple changepoint model

library(rjags)

# Specify the model and save to a file
model.string <- "
model {

  c[1] <- 0
  a[1] <- 1

  for (i in 2:N) {
    c[i] ~ dbern(p.c[i])  # is there a changepoint at time index i?
    a[i] ~ dcat(p.a[a[i-1],,c[i]+1])
  }  

  
}
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list()

# Data
p.c <- c(rep(0,5), rep(0.1,5))
p.a <- array(0, dim = c(2,2,2))
p.a[,,1] <- matrix(c(1,0,0,1), nrow=2)
p.a[,,2] <- matrix(c(0,0,1,1), nrow=2)

data <- list(N = 10,
             p.c = p.c, 
             p.a = p.a)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    inits = inits, n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("c", "a"), n.iter = 1000)
#plot(samples)

m <- as.matrix(samples)
head(m)
