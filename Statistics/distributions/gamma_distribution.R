# Gamma distribution
# Code from
# http://doingbayesiandataanalysis.blogspot.co.uk/2012/08/gamma-likelihood-parameterized-by-mode.html

library(rjags)

# Specify the model and save to a file
model.string <- "
model {
  k ~ dgamma(sh, ra)

  # Calculate the shape and rate parameters from:
  # m = mode
  # sd = standard deviaton
  sh <- 1 + m * ra
  ra <- ( m + sqrt( m^2 + 4*sd^2 ) ) / ( 2 * sd^2 )
}
"
writeLines(model.string, con = "temp_model.txt")

# Initialisation
inits <- list("k" = 1)

# Data
data <- list(m = 2, sd = 4)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    inits = inits, n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, variable.names = c("k"), n.iter = 1000)
plot(samples)
summary(samples)