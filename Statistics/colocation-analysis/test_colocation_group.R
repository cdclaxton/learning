library(testthat) 

source('colocation_group.R')
context('Colocation group')

# calc.centroid()
# ------------------------------------------------------------------------------

test_that("calc.centroid should work for a single point", {
  lats <- c(10)
  longs <- c(3)
  indices <- c(1)
  
  result <- calc.centroid(lats, longs, indices)
  expected <- c(10, 3)
  expect_true(all.equal(result, expected))
})

test_that("calc.centroid should work for two points, but one index", {
  lats <- c(10, 20)
  longs <- c(3, 5)
  indices <- c(1)
  
  result <- calc.centroid(lats, longs, indices)
  expected <- c(10, 3)
  expect_true(all.equal(result, expected))
})

test_that("calc.centroid should work for two points and two indices", {
  lats <- c(10, 20)
  longs <- c(3, 5)
  indices <- c(1,2 )
  
  result <- calc.centroid(lats, longs, indices)
  expected <- c(15, 4)
  expect_true(all.equal(result, expected))
})

# calc.colocation.groups()
# ------------------------------------------------------------------------------

test_that("calc.colocation.groups should work for a single point", {
  C <- matrix(c(FALSE), nrow = 1, ncol = 1)
  
  result <- calc.colocation.groups(C)
  expected <- list()
  expect_true(all.equal(result, expected))
})

test_that("calc.colocation.groups should work for two points that are colocated", {
  C <- matrix(c(FALSE, TRUE, FALSE, FALSE), nrow = 2)
  
  result <- calc.colocation.groups(C)
  expected <- list(c(1,2))
  expect_true(all.equal(result, expected))
})

test_that("calc.colocation.groups should work for two points that are not colocated", {
  C <- matrix(c(FALSE, FALSE, FALSE, FALSE), nrow = 2)
  
  result <- calc.colocation.groups(C)
  expected <- list()
  expect_true(all.equal(result, expected))
})

test_that("calc.colocation.groups should work for two points that are colocated", {
  C <- matrix(c(FALSE, TRUE, FALSE, FALSE), nrow = 2)
  
  result <- calc.colocation.groups(C)
  expected <- list(c(1,2))
  expect_true(all.equal(result, expected))
})

test_that("calc.colocation.groups should work for three points that are colocated (1 group, 2 samples)", {
  C <- matrix(c(FALSE, FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE), nrow = 3)
  
  result <- calc.colocation.groups(C)
  expected <- list(c(1,3))
  expect_true(all.equal(result, expected))
})

test_that("calc.colocation.groups should work for three points that are colocated (1 group, 3 samples)", {
  C <- matrix(c(FALSE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE), nrow = 3)
  
  result <- calc.colocation.groups(C)
  expected <- list(c(1,2,3))
  expect_true(all.equal(result, expected))
})

test_that("calc.colocation.groups should work for three points that are colocated (2 groups)", {
  C <- matrix(c(FALSE, TRUE, FALSE, FALSE, FALSE, TRUE, FALSE, FALSE, FALSE), nrow = 3)
  
  result <- calc.colocation.groups(C)
  expected <- list(c(1,2), c(2,3))
  expect_true(all.equal(result, expected))
})

# calc.colocation.groups.centroids()
# ------------------------------------------------------------------------------

test_that("calc.colocation.groups.centroids works for a group with a single entry", {
  lats <- c(10)
  longs <- c(4)
  groups <- list(c(1))
  
  result <- calc.colocation.groups.centroids(lats, longs, groups)
  expected <- data.frame(lat = c(10), long = c(4))
  expect_true(all.equal(result, expected))
})

test_that("calc.colocation.groups.centroids works for a group with a single entry with extra coords", {
  lats <- c(10, 100)
  longs <- c(4, 400)
  groups <- list(c(1))
  
  result <- calc.colocation.groups.centroids(lats, longs, groups)
  expected <- data.frame(lat = c(10), long = c(4))
  expect_true(all.equal(result, expected))
})

test_that("calc.colocation.groups.centroids works for a group with two entries", {
  lats <- c(10, 100, 12)
  longs <- c(4, 400, 6)
  groups <- list(c(1, 3))
  
  result <- calc.colocation.groups.centroids(lats, longs, groups)
  expected <- data.frame(lat = c(11), long = c(5))
  expect_true(all.equal(result, expected))
})

test_that("calc.colocation.groups.centroids works for two groups", {
  lats <- c(10, 100, 12)
  longs <- c(4, 400, 6)
  groups <- list(c(1, 3), c(2))
  
  result <- calc.colocation.groups.centroids(lats, longs, groups)
  expected <- data.frame(lat = c(11, 100), long = c(5, 400))
  expect_true(all.equal(result, expected))
})
