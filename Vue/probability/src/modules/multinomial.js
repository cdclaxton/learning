/**
 * Build a Cumulative Probability Function (CDF) from a PDF.
 * @param {array} probabilities Array of probabilities.
 * @returns CDF.
 */
export function buildCdf(probabilities) {
  if (probabilities.length === 0) {
    throw new Error('no probabilities')
  }

  // Check each of the probabilities are valid
  for (let p of probabilities) {
    if (p < 0.0 || p > 1.0) {
      throw new Error('invalid probability')
    }
  }

  // Check the total probability is within tolerance
  let total = probabilities.reduce((a, b) => a + b)
  if (Math.abs(total - 1.0) > 1e-6) {
    throw new Error('probabilities do not sum to 1')
  }

  let cdf = []
  cdf.push(probabilities[0])
  for (let i = 1; i < probabilities.length; i++) {
    cdf.push(cdf[i - 1] + probabilities[i])
  }

  return cdf
}

/**
 * Largest index where cdf[index] <= u.
 * @param {*} cdf CDF.
 * @param {*} u Probability.
 * @returns Index.
 */
export function largestIndex(cdf, u) {
  if (u <= cdf[0]) {
    return 0
  }

  for (let i = 1; i < cdf.length; i++) {
    if (u <= cdf[i]) {
      return i
    }
  }

  return cdf.length - 1
}

/**
 * Draw a sample from a CDF.
 * @param {array} cdf Cumulative probability distribution.
 * @returns Sample index.
 */
export function sampleFromCDF(cdf) {
  // Draw a sample from a uniform distribution in the range [0,1]
  let u = Math.random()

  return largestIndex(cdf, u)
}

/**
 * Sample from a multinomial distribution.
 * @param {array} values Array of values.
 * @param {array} probabilities Array of probabilities.
 * @param {int} n Number of samples to generate.
 * @returns Array of samples from the multinomial distribution.
 */
export function sampleMultinomialPMF(values, probabilities, n) {
  // Check the inputs
  if (values.length !== probabilities.length) {
    throw new Error('inconsistent values and probabilities')
  } else if (n < 0) {
    throw new Error('invalid number of samples')
  }

  // Build the CDF
  let cdf = buildCdf(probabilities)

  // Sample from the CDF
  let samples = []
  for (let i = 0; i < n; i++) {
    let idx = sampleFromCDF(cdf)
    samples.push(values[idx])
  }

  // Return the samples
  return samples
}
