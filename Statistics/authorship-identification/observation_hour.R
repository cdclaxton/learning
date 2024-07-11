# Observations of the time of an event.
#
# Assume a uniform distribution. For simplicity, it's assumed that there
# are only four time periods in a day.

library(rjags)

# Generate the observations
N <- 20
h <- sample(3:4, size = N, replace = TRUE)

# Specify the model and save to a file
model.string <- "
  model {

    # Prior (Dirchlet prior)
    for (i in 1:4) {
      theta[i] <- 1/4
    }
    p ~ ddirch(theta)

    # Training samples
    for (i in 1:N) {
      h[i] ~ dcat(p)
    }

    h.prime ~ dcat(p)
  }
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
#inits <- list("h" = 1)

data <- list("h" = h, # Samples
             "N" = N) # Number of samples

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, 
                        variable.names = c("p", "h", "h.prime"), 
                        n.iter = 1000)
plot(samples)
summary(samples)

m <- as.matrix(samples)
hist(m[,"h.prime"])
