library(testthat) 

source('visualisation.R')
context('Visualisation')

# bounding.box()
# ------------------------------------------------------------------------------

test_that("bounding.box should work for two coordinates", {
  lats <- c(51.514371, 51.520116)
  longs <- c(-2.548903, -2.525042)
  
  result <- bounding.box(lats, longs)
  expected <- c(-2.548903, 51.514371, -2.525042, 51.520116)
  expect_true(all.equal(result, expected))
})