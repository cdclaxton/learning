# Example 3.4.1: Three coins
#
# 3 coins (equally likely to be chosen)
# p(heads | coin 1) = 0.25
# p(heads | coin 2) = 0.50
# p(heads | coin 3) = 0.75
#
# Randomly select one coin --> head

library(rjags)

# Specify the model and save to a file
model.string <- "
model {
  for (i in 1:3) {
    p[i] <- 1/3
    theta[i] <- 0.25 * i
    coin.prob[i] <- equals(coin, i)
  }

  y ~ dbern(theta.true)  # observation
  theta.true <- theta[coin]
  coin ~ dcat(p[])

  Y.pred ~ dbern(theta.true)  # p(Y = 1 | y) <-- prediction
}
"
writeLines(model.string, con = "temp_model.txt")

data <- list("y" = 1)  # observed one head

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, 
                        variable.names = c("coin.prob", "Y.pred"), 
                        n.iter = 1000)
plot(samples)
summary(samples)