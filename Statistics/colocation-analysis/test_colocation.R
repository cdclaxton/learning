library(testthat) 

source('colocation.R')
context('Colocation')

# threshold.lower.tri.matrix()
# ------------------------------------------------------------------------------

test_that("threshold.lower.tri.matrix should work for a 2x2 matrix",{
  M <- matrix(c(10, 20, 30, 40), nrow = 2)
  thresholded <- threshold.lower.tri.matrix(M, 35)
  expected <- matrix(c(0,1,0,0), nrow = 2)
  expect_true(all.equal(thresholded, expected))
})

test_that("threshold.lower.tri.matrix should work for a 3x3 matrix",{
  M <- matrix(c(20, 20, 20, 10, 20, 20, 10, 10, 20), nrow = 3)
  thresholded <- threshold.lower.tri.matrix(M, 15)
  expected <- matrix(c(0), nrow=3, ncol=3)
  expect_true(all.equal(thresholded, expected))
})

test_that("threshold.lower.tri.matrix should throw an exception for an non-square matrix",{
  M <- matrix(c(20, 20, 20, 10, 20, 20, 10, 10, 20, 20), nrow = 2)
  expect_error(threshold.lower.tri.matrix(M, 15))
})

# calc.time.differences()
# ------------------------------------------------------------------------------

test_that("calc.time.differences works correctly for a single time entry", {
  times <- c(10)
  result <- calc.time.differences(times)
  expected <- matrix(c(0), nrow = 1)
  expect_true(all.equal(result, expected))
})

test_that("calc.time.differences works correctly for two time entries", {
  times <- c(10, 20)
  result <- calc.time.differences(times)
  expected <- matrix(c(0, 10, 0, 0), nrow = 2)
  expect_true(all.equal(result, expected))
})

test_that("calc.time.differences works correctly for three time entries", {
  times <- c(10, 20, 10)
  result <- calc.time.differences(times)
  expected <- matrix(c(0, 10, 0, 0, 0, 10, 0, 0, 0), nrow = 3)
  expect_true(all.equal(result, expected))
})

# calc.geo.distances()
# ------------------------------------------------------------------------------

test_that("calc.geo.distances should throw an exception if the lats and longs are different lengths", {
  lats <- c(1)
  longs <- c(1,2)
  expect_error(calc.geo.distances(lats, longs))
})

test_that("calc.geo.distances should work correctly for a single point", {
  lats <- c(1)
  longs <- c(1)
  result <- calc.geo.distances(lats, longs)
  expected <- matrix(c(0), nrow = 1, ncol = 1)
  expect_true(all.equal(result, expected))
})

test_that("calc.geo.distances should work correctly for two points", {
  lats <- c(1, 4)
  longs <- c(1, 5)
  result <- calc.geo.distances(lats, longs)
  expected <- matrix(c(0, 5, 0, 0), nrow = 2)
  expect_true(all.equal(result, expected))
})

# calc.near.in.space()
# ------------------------------------------------------------------------------

test_that("calc.near.in.space should work correctly for a single sample", {
  lats <- c(100)
  longs <- c(20)
  result <- calc.near.in.space(lats, longs, 10)
  expected <- matrix(c(0), nrow = 1, ncol = 1)
  expect_true(all.equal(result, expected))
})

test_that("calc.near.in.space should work correctly for two sample outside threshold", {
  lats <- c(100, 200)
  longs <- c(20, 40)
  result <- calc.near.in.space(lats, longs, 10)
  expected <- matrix(c(0, 0, 0, 0), nrow = 2)
  expect_true(all.equal(result, expected))
})

test_that("calc.near.in.space should work correctly for two sample inside threshold", {
  lats <- c(100, 103)
  longs <- c(20, 24)
  result <- calc.near.in.space(lats, longs, 6)
  expected <- matrix(c(0, 1, 0, 0), nrow = 2)
  expect_true(all.equal(result, expected))
})


# calc.near.in.time()
# ------------------------------------------------------------------------------

test_that("calc.near.in.time should work correctly for a single sample", {
  times <- c(100)
  result <- calc.near.in.time(times, 10)
  expected <- matrix(c(0), nrow = 1, ncol = 1)
  expect_true(all.equal(result, expected))
})

test_that("calc.near.in.time should work correctly for two samples outside threshold", {
  times <- c(100, 140)
  result <- calc.near.in.time(times, 20)
  expected <- matrix(c(0, 0, 0, 0), nrow = 2)
  expect_true(all.equal(result, expected))
})

test_that("calc.near.in.time should work correctly for two samples inside threshold", {
  times <- c(100, 110)
  result <- calc.near.in.time(times, 20)
  expected <- matrix(c(0, 1, 0, 0), nrow = 2)
  expect_true(all.equal(result, expected))
})

# colocated()
# ------------------------------------------------------------------------------

test_that("colocated should work for a single sample", {
  lats <- c(100)
  longs <- c(20)
  times <- c(100)
  delta.d <- 10
  delta.t <- 5
  result <- colocated(lats, longs, times, delta.d, delta.t)
  
  expected.N.time <- matrix(c(0), nrow = 1, ncol = 1)
  expect_true(all.equal(result$N.time, expected.N.time))
  
  expected.N.space <- matrix(c(0), nrow = 1, ncol = 1)
  expect_true(all.equal(result$N.space, expected.N.space))
  
  expected.C <- matrix(c(FALSE), nrow = 1, ncol = 1)
  expect_true(all.equal(result$C, expected.C))
})

test_that("colocated should work for two colocated sample", {
  lats <- c(100, 103)
  longs <- c(20, 24)
  times <- c(100, 200)
  delta.d <- 6
  delta.t <- 150
  result <- colocated(lats, longs, times, delta.d, delta.t)
  
  expected.N.time <- matrix(c(0, 1, 0, 0), nrow = 2)
  expect_true(all.equal(result$N.time, expected.N.time))
  
  expected.N.space <- matrix(c(0, 1, 0, 0), nrow = 2)
  expect_true(all.equal(result$N.space, expected.N.space))
  
  expected.C <- matrix(c(FALSE, TRUE, FALSE, FALSE), nrow = 2)
  expect_true(all.equal(result$C, expected.C))
})

test_that("colocated should work for two samples that aren't colocated due to time", {
  lats <- c(100, 103)
  longs <- c(20, 24)
  times <- c(100, 200)
  delta.d <- 6
  delta.t <- 50
  result <- colocated(lats, longs, times, delta.d, delta.t)
  
  expected.N.time <- matrix(c(0, 0, 0, 0), nrow = 2)
  expect_true(all.equal(result$N.time, expected.N.time))
  
  expected.N.space <- matrix(c(0, 1, 0, 0), nrow = 2)
  expect_true(all.equal(result$N.space, expected.N.space))
  
  expected.C <- matrix(c(FALSE, FALSE, FALSE, FALSE), nrow = 2)
  expect_true(all.equal(result$C, expected.C))
})

test_that("colocated should work for two samples that aren't colocated due to space", {
  lats <- c(100, 103)
  longs <- c(20, 24)
  times <- c(100, 130)
  delta.d <- 4
  delta.t <- 50
  result <- colocated(lats, longs, times, delta.d, delta.t)
  
  expected.N.time <- matrix(c(0, 1, 0, 0), nrow = 2)
  expect_true(all.equal(result$N.time, expected.N.time))
  
  expected.N.space <- matrix(c(0, 0, 0, 0), nrow = 2)
  expect_true(all.equal(result$N.space, expected.N.space))
  
  expected.C <- matrix(c(FALSE, FALSE, FALSE, FALSE), nrow = 2)
  expect_true(all.equal(result$C, expected.C))
})