# ------------------------------------------------------------------------------
# Graphical Independence Networks
#
#
# To use:
# source("https://bioconductor.org/biocLite.R")
# biocLite("RBGL")
# biocLite("Rgraphviz")
# install.packages("gRain")
# 
# install.packages('hash')
#
# To install RNetica:
# - Download ZIP file: http://pluto.coe.fsu.edu/RNetica/RNetica_0.4-4.zip
# - Copy RNetica folder within ZIP to local R repo, e.g.
#   C:\Users\Christopher\Documents\R\win-library\3.3
# 
# Download and install Netica:
# - Download from https://www.norsys.com/download.html
# ------------------------------------------------------------------------------

library(gRain)


# Just a single variable (80% probability of being cloudy)
# ------------------------------------------------------------------------------
c <- cptable(~ cloudy, values = c(0.8,0.2), levels = c("yes", "no"))
(plist <- compileCPT(list(c)))
plist$cloudy

# Sprinkler example
# ------------------------------------------------------------------------------

c <- cptable(~ cloudy, values = c(0.5,0.5), levels = c("yes", "no"))
s <- cptable(~ sprinkler | cloudy, values = c(0.1, 0.9, 0.5, 0.5), levels=c("yes", "no"))
r <- cptable(~ rain | cloudy, values = c(0.8, 0.2, 0.2, 0.8), levels=c("yes", "no"))
w <- cptable(~ wetgrass | sprinkler + rain, values = c(0.99, 0.01, 0.9, 0.1, 0.9, 0.1, 0.0, 1.0), levels=c("yes", "no"))
(plist <- compileCPT(list(c, s, r, w)))
plist$cloudy
plist$sprinkler
plist$rain
plist$wetgrass
gin1 <- grain(plist)
summary(gin1)

# Enter findings
gin1.find <- setFinding(gin1, nodes = c("wetgrass"), states = c("yes"))
querygrain(gin1.find, nodes = c("sprinkler"), type = "marginal")
querygrain(gin1.find, nodes = c("rain"), type = "marginal")                       
