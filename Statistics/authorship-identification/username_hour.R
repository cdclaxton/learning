# Authorship identification model with multiple usernames

library(ggplot2)
library(rjags)
library(reshape2)

gen.observations <- function(p.user, cpt, N) {
  # Generate observations.
  # 
  # Args:
  #   p.user: Vector of the probability of each user posting.
  #   cpt: n.users x n.slots Conditonal Probability Table.
  #   N: Number of samples to generate.
  #
  # Returns:
  #   Dataframe of user ID and time slot.
  
  # Preconditions
  stopifnot(length(p.user) == nrow(cpt))
  stopifnot(sum(p.user) == 1)
  stopifnot(N > 0)
  
  # Create the dataframe
  df <- data.frame(userId = rep(NA, N),
                   timeslot = rep(NA, N))
  
  # Populate the dataframe
  for (i in 1:N) {
    userId <- which(rmultinom(1, 1, p.user) == 1)
    timeslot <- which(rmultinom(1, 1, cpt[userId, ]) == 1)
    
    df[i,]$userId <- userId
    df[i,]$timeslot <- timeslot
  }
  
  # Postconditions
  stopifnot(nrow(df) == N)
  
  # Return the dataframe
  df
}

p.user <- c(0.6, 0.3, 0.1)
cpt <- t(matrix(c(0.8,0.2, 0.5,0.5, 0.1,0.9), ncol = 3))
num.observations <- 1000
df <- gen.observations(p.user, cpt, num.observations)

# Specify the JAGS model
model.string <- "model {
  p.u ~ ddirch(alpha.u)  # username prior

  # Training samples
  for (i in 1:N.sample) {
    u[i] ~ dcat(p.u)  # username
    t[i] ~ dcat(p.t[u[i],1:N.timeslots])  # time slot
  }

  # Test sample (given a forum post, which user posted it?)
  u.test ~ dcat(p.u)  # username (unknown)
  t.test ~ dcat(p.t[u.test,1:N.timeslots])  # time slot (known)

  # Prior for the time slot for the j(th) user
  for (j in 1:N.user) {
    alpha[j,1:N.timeslots] <- alpha.t
    p.t[j,1:N.timeslots] ~ ddirch(alpha[j,1:N.timeslots])
  }

  # Prediction of the probability of users posting (for graphing purposes)
  u.pred ~ dcat(p.u)

  # Prediction of the times a given user will post (for graphing purposes)
  for (j in 1:N.user) {
    t.pred[j] ~ dcat(p.t[j,1:N.timeslots])
  }

}
"

# Save the JAGS model to a file
writeLines(model.string, con = "temp_model.txt")

# Specify the (training and test) data
N.user <- length(p.user)
N.timeslots <- ncol(cpt)
test.timeslot <- 1
data <- list(alpha.u = rep(1/N.user, N.user),
             alpha.t = rep(1/N.timeslots, N.timeslots),
             N.sample = nrow(df),
             N.user = N.user,
             N.timeslots = N.timeslots,
             u = df$userId,
             t = df$timeslot,
             t.test = test.timeslot)

# Build the JAGS model
model <- jags.model(file = "temp_model.txt", data = data,
                    n.chains = 1, n.adapt = 500)
update(model, n.iter = 500)
samples <- coda.samples(model, 
                        variable.names = c("u.pred", "t.pred", "u.test"), 
                        n.iter = 10000)
plot(samples)
summary(samples)

m <- as.matrix(samples)

# Plot the probability of each user submitting a forum post
df1.expected <- data.frame(user = 1:length(p.user),
                           expected = p.user)
ggplot(data.frame(value = m[,"u.pred"]), aes(value)) + 
  geom_bar(aes(y = (..count..)/sum(..count..))) +
  geom_point(data = df1.expected, aes(user, expected), color = "red") +
  geom_line(data = df1.expected, aes(user, expected), linetype = "dotted") +
  xlab("User index") +
  ylab("Proportion of posts")

# Plot the probability of the time slot in which a given user posts
# There is probably a better way of doing this using the aggregate function.
actual <- matrix(ncol = length(p.user) + 1, 
                nrow = ncol(cpt))
actual[,1] <- 1:ncol(cpt)  # timeslot
colnames(actual) <- 1:ncol(actual)
colnames(actual)[1] <- "timeslot"
actual <- data.frame(actual)

expected <- matrix(ncol = length(p.user) + 1, 
                 nrow = ncol(cpt))
expected[,1] <- 1:ncol(cpt)  # timeslot
colnames(expected) <- 1:ncol(expected)
colnames(expected)[1] <- "timeslot"
expected <- data.frame(expected)

for (i in 1:length(p.user)) {
  # Create the column name
  col.name <- paste0("user", i)
  names(actual)[i+1] <- col.name
  names(expected)[i+1] <- col.name
  
  count <- m[, paste0("t.pred[", i, "]")]
  
  # Walk over each time index
  for (timeindex in 1:ncol(cpt)) {
    actual[timeindex, col.name] <- length(which(count == timeindex)) / length(count)
    expected[timeindex, col.name] <- cpt[i,timeindex]
  }
} 

actual$type <- rep("actual", nrow(actual))
actual.melt <- melt(actual, id.vars = c("timeslot", "type"))

expected$type <- rep("expected", nrow(actual))
expected.melt <- melt(expected, id.vars = c("timeslot", "type"))

all <- rbind(actual.melt, expected.melt)

ggplot(data = all) +
  geom_point(aes(x = timeslot, y = value, color = type)) +
  geom_line(aes(x = timeslot, y = value, color = type)) +
  facet_wrap( ~ variable) +
  xlab("Timeslot") + ylab("Probability of posting during timeslot")
  
# Plot the probability that the post was due to each user
df2 <- data.frame(user = 1:length(p.user),
                  prob = rep(NA, length(p.user)))
for (user in 1:length(p.user)) {
  df2[user,]$prob <- length(which(m[, "u.test"] == user))
}
df2$prob <- df2$prob / nrow(m)

ggplot(df2, aes(user, prob)) +
  geom_bar(stat = "identity") +
  xlab("User") + 
  ylab(paste0("Probability user posted at timeslot ", test.timeslot))

