# Hidden Markov Model
#
# 2 regime market (bullish or bearish)
# Normally distributed market returns
# N_k days of returns
# 
# Required libraries:
# install.packages('depmixS4')

# Clear the environment
rm(list=ls())
library('depmixS4')

# Set the seed to allow for consistent results
set.seed(1)

# Create the parameters for the bull and bear market returns
Nk_lower <- 50
Nk_upper <- 150
bull_mean <- 0.1
bull_var <- 0.1
bear_mean <- -0.05
bear_var <- 0.2

# Create the list of durations (in days) for each regime
days <- replicate(5, sample(Nk_lower:Nk_upper, 1))

# Create the bull and bear market returns
market_bull_1 <- rnorm(days[1], bull_mean, bull_var)
market_bear_2 <- rnorm(days[2], bear_mean, bear_var)
market_bull_3 <- rnorm(days[3], bull_mean, bull_var)
market_bear_4 <- rnorm(days[4], bear_mean, bear_var)
market_bull_5 <- rnorm(days[5], bull_mean, bull_var)

# Create the list of true regime states and full returns list
true_regimes <- c(rep(1,days[1]),rep(2,days[2]), 
                  rep(1,days[3]),rep(2,days[4]),
                  rep(1,days[1]))

returns <- c(market_bull_1, market_bear_2,
             market_bull_3, market_bear_4,
             market_bull_5)

# Plot the returns
plot(returns, type="l", xlab='', ylab="Returns")
for (i in 1:5) {
  time <- cumsum(days)[i]
  lines(x = c(time, time), y = c(min(returns), max(returns)),
        col="red")
}

# Fit the HMM using EM
hmm <- depmix(returns ~ 1, family = gaussian(), nstates = 2, 
              data=data.frame(returns=returns))
hmmfit <- fit(hmm, verbose = FALSE)

# Show the posterior probabilities
post_probs <- posterior(hmmfit)
layout(1:2)
plot(post_probs$state, type = 's', main = 'True regimes', 
     xlab = '', ylab = 'Regime')
matplot(post_probs[,-1], type = 'l', main = "Regime posterior probabilities",
        ylab = 'Probability')
legend(x='left', c('Bull', 'Bear'), fill = 1:2, bty = 'n')