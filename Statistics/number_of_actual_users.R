# Estimate the number of actual users using a Bayesian approach
#
# Setup:
# install.packages("ggplot2")
# install.packages("rjags")
# ------------------------------------------------------------------------------

rm(list=ls(all=TRUE))

library(ggplot2)
library(rjags)

# ------------------------------------------------------------------------------
# Generate the synthetic data
# ------------------------------------------------------------------------------

# Number of actual users
nu <- 500

# Number of usernames per user
ppu <- 20

# Number of usernames
n <- ceiling(nu * ppu)

# Proportion of the usernames observed
prop <- 0.05

# Number of observed usernames
obs <- ceiling(n * prop)

# ------------------------------------------------------------------------------
# Perform inference
# ------------------------------------------------------------------------------

# Specify the model and save to a file
model.string <- "
model {
  
  # Actual number of users (Poisson distribution with a Gamma prior)
  # Calculate the shape and rate parameters from: mode; std. dev.
  nu.sh <- 1 + nu.m * nu.ra
  nu.ra <- ( nu.m + sqrt( nu.m^2 + 4*nu.sd^2 ) ) / ( 2 * nu.sd^2 )  
  lambda.nu ~ dgamma(nu.sh, nu.ra)
  
  nu ~ dpois(lambda.nu)

  # Average number of usernames per user
  ppu.sh <- 1 + ppu.m * ppu.ra
  ppu.ra <- ( ppu.m + sqrt( ppu.m^2 + 4*ppu.sd^2 ) ) / ( 2 * ppu.sd^2 )

  ppu ~ dgamma(ppu.sh, ppu.ra)

  # Number of usernames
  n <- nu * ppu #round(nu * ppu)

  # Proportion of usernames observed (Beta distribution)
  prop ~ dunif(0,0.3)

  # Number of usernames observed
  obs <- n * prop

  # Slightly noisy version of the number of usernames observed
  obs.noise ~ dnorm(obs, 0.01)
}
"
writeLines(model.string, con = "temp_model.txt")

# Data
nu.m <- 1000
nu.sd <- 400
ppu.m <- 20
ppu.sd <- 10

data.before <- list(nu.m = nu.m, nu.sd = nu.sd, 
             ppu.m = ppu.m, ppu.sd = ppu.sd)

data.after <- list(nu.m = nu.m, nu.sd = nu.sd, 
                   ppu.m = ppu.m, ppu.sd = ppu.sd,
                   obs.noise = obs)

# Initialisation
inits <- list("nu" = 1000)

# Build the JAGS model
model.before <- jags.model(file = "temp_model.txt", data = data.before,
                    inits = inits, n.chains = 4, n.adapt = 400000)

model.after <- jags.model(file = "temp_model.txt", data = data.after,
                          inits = inits, n.chains = 4, n.adapt = 400000)

update(model.before, n.iter = 10000)
update(model.after, n.iter = 10000)

variable.names = c("lambda.nu", "nu", "ppu", "n", "prop")

samples.before <- coda.samples(model.before,
                               variable.names = variable.names,
                               n.iter = 200000, thin = 100)

samples.after <- coda.samples(model.after,
                              variable.names = variable.names,
                              n.iter = 200000, thin = 100)

plot(samples.before)
plot(samples.after)

# Extract the values
m.before <- as.matrix(samples.before)
m.after <- as.matrix(samples.after)

plot.hists <- function(before, after, name) {
  b <- data.frame(value = before)
  a <- data.frame(value = after)
  b$name <- "before"
  a$name <- "after"
  both <- rbind(b,a)
  ggplot(both, aes(value, fill = name)) + geom_density(alpha = 0.2) +
    labs(x = name)
}

# Plot the distribution of the actual number of users
plot.hists(m.before[,"nu"], m.after[,"nu"], "Number of users")
plot.hists(m.before[,"n"], m.after[,"n"], "Number of usernames")
plot.hists(m.before[,"prop"], m.after[,"prop"], "Proportion of usernames observed")
plot.hists(m.before[,"ppu"], m.after[,"ppu"], "Usernames per user")

cat("Mean number of users = ", mean(m.after[,"nu"]), "\n")
cat("Mean number of usernames per user = ", mean(m.after[,"ppu"]), "\n")
cat("Mean number of profiles = ", mean(m.after[,"n"]), "\n")
cat("Proportion of usernames observed = ", mean(m.after[,"prop"]), "\n")

# Check for convergence
gelman.diag(samples.before)
gelman.diag(samples.after)
