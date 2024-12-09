/**
 * Represents a (value, probability) tuple.
 * @param {number} value
 * @param {number} probability in the range [0, 1].
 */
export class ProbabilityElement {
  constructor(value, probability) {
    // Check that the probability is valid
    if (probability < 0 || probability > 1) {
      throw new RangeError(`invalid probability: ${probability}`)
    }

    this.value = value
    this.probability = probability
  }
}

/**
 * Returns true if the values are unique.
 * @param {number[]} values
 * @returns {boolean} True if the values are unique, otherwise false.
 */
export function hasUniqueValues(values) {
  let s = new Set(values)
  return s.size === values.length
}

/**
 * Returns true if the probabilities sum to unity and each probability is valid.
 * @param {number[]} probabilities
 * @returns {boolean} True if the probabilities are well-formed
 */
export function probabilitiesValid(probabilities) {
  // Check each probability
  for (let p of probabilities) {
    if (p < 0 || p > 1) {
      return false
    }
  }

  // Check the total probability
  let total = probabilities.reduce((a, b) => a + b, 0)
  return Math.abs(total - 1.0) < 1e-6
}

/**
 * Probability distribution.
 */
export class Distribution {
  constructor(values, probabilities) {
    if (values.length === 0) {
      throw new Error('no values')
    }

    // Check that the values and the probabilities are consistent
    if (values.length !== probabilities.length) {
      throw new Error(
        `values and probabilities have differing lengths: ${values.length} and ${probabilities.length}`,
      )
    }

    // Check there are no duplicate values
    if (!hasUniqueValues(values)) {
      throw new Error('values are not unique')
    }

    // Check the probabilities are valid
    if (!probabilitiesValid(probabilities)) {
      throw new Error(`invalid probabilities: ${probabilities}`)
    }

    this.values = values
    this.probabilities = probabilities
  }

  equals(other, tolerance) {
    return distributionsInTolerance(this, other, tolerance)
  }
}

/**
 * Returns true if both arrays have identical lengths and values.
 * @param {number[]} values1
 * @param {number[]} values2
 * @returns {boolean}
 */
export function valuesEqual(values1, values2) {
  if (values1.length !== values2.length) {
    return false
  }

  for (let i in values1) {
    if (values1[i] !== values2[i]) {
      return false
    }
  }

  return true
}

/**
 * Returns true if the probability vectors have the same length and the values
 * are within tolerance.
 * @param {number[]} probs1 Array of probabilities
 * @param {number[]} probs2 Array of probabilities
 * @param {number} tolerance Tolerance >= 0
 * @returns {boolean}
 */
export function probabilitiesInTolerance(probs1, probs2, tolerance) {
  if (tolerance < 0.0) {
    throw new RangeError(`tolerance is invalid: ${tolerance}`)
  }

  if (probs1.length !== probs2.length) {
    return false
  }

  for (let i in probs1) {
    let delta = Math.abs(probs1[i] - probs2[i])
    if (delta > tolerance) {
      return false
    }
  }

  return true
}

/**
 * Checks if the two distributions are within tolerance. The values must match
 * exactly, but the probabilities can differ by the specified tolerance.
 * @param {Distribution} dist1 Probability distribution 1
 * @param {Distribution} dist2 Probability distribution 2
 * @param {number} tolerance
 * @returns
 */
export function distributionsInTolerance(dist1, dist2, tolerance) {
  if (tolerance < 0.0) {
    throw new RangeError(`tolerance is invalid: ${tolerance}`)
  }

  if (!valuesEqual(dist1.values, dist2.values)) {
    return {
      success: false,
      message: `values are not equal: ${dist1.values} vs ${dist2.values}`,
    }
  }

  if (!probabilitiesInTolerance(dist1.probabilities, dist2.probabilities, tolerance)) {
    return {
      success: false,
      message: `probabilities are not equal: ${dist1.probabilities} vs ${dist2.probabilities}`,
    }
  }

  return {
    success: true,
    message: '',
  }
}
