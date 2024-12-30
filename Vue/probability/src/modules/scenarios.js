/**
 * ProbabilityInput holds and parses the string value for a probability.
 */
export class ProbabilityInput {
  constructor(value) {
    this.stringValue = value
  }

  /**
   * Checks if the probability is valid.
   * @returns True if the probability is valid.
   */
  isValid() {
    return !Number.isNaN(this.probability())
  }

  /**
   * Parse the string representation of the probability.
   * @returns Probability in the range [0,1] or NaN if it is invalid.
   */
  probability() {
    let p = parseFloat(this.stringValue)
    if (Number.isNaN(p)) {
      return NaN
    } else if (p < 0.0 || p > 1.0) {
      return NaN
    }

    return p
  }

  /**
   * Returns true if the other probability equals this probability.
   * @param {Number} other Other probability.
   * @returns True if the other probability equals this probability.
   */
  equals(other) {
    let p = this.probability()
    return (Number.isNaN(other) && Number.isNaN(p)) || Math.abs(p - other) < 1e-6
  }
}

/**
 * ValueInput holds and parses a floating point value.
 */
export class ValueInput {
  constructor(value) {
    this.stringValue = value
  }

  /**
   * Returns true if the value is valid, i.e. it can be parsed to a float.
   * @returns True if the value is valid.
   */
  isValid() {
    return !Number.isNaN(this.value())
  }

  /**
   * Get the parsed floating point value.
   * @returns Parsed value as a float, otherwise NaN.
   */
  value() {
    return parseFloat(this.stringValue)
  }

  /**
   * Returns true if the other value equals this value.
   * @param {float} other Other value (float or NaN).
   * @returns True if the other value equals this value.
   */
  equals(other) {
    let v = this.value()
    return (Number.isNaN(other) && Number.isNaN(v)) || Math.abs(v - other) < 1e-6
  }
}

/**
 * DistributionElement holds the value and its probability and is an element of
 * a discrete probability distribution.
 */
export class DistributionElement {
  constructor(value, probability) {
    this.valueInput = new ValueInput(value)
    this.probabilityInput = new ProbabilityInput(probability)
  }

  /**
   * Checks both the value and its associated probability for validity.
   * @returns True if both the value and the probability are valid.
   */
  isValid() {
    return this.valueInput.isValid() && this.probabilityInput.isValid()
  }

  /**
   * Checks if the value and its associated probability are within tolerance.
   * @param {float} otherValue Other value.
   * @param {float} otherProbability Other probability.
   * @returns True if the values and probabilities are within tolerance.
   */
  equals(otherValue, otherProbability) {
    return this.valueInput.equals(otherValue) && this.probabilityInput.equals(otherProbability)
  }
}

/**
 * Discrete probability distribution.
 */
export class DiscreteDistribution {
  constructor(config) {
    this.elements = []

    for (let value in config) {
      this.elements.push(new DistributionElement(value, config[value]))
    }
  }

  /**
   * Add an element to the distribution.
   */
  addElement(value, probability) {
    this.elements.push(new DistributionElement(value, probability))
  }

  /**
   * Delete an element from the distribution.
   * @param idx Index of the element to remove.
   * @returns True if the element was removed.
   */
  deleteElement(idx) {
    if (idx < 0 || idx >= this.elements.length) {
      return false
    }

    this.elements.splice(idx, 1)
    return true
  }

  /**
   * Calculate the total probability of the distribution elements.
   * @returns Total probaility or NaN if an invalid probability is encountered.
   */
  totalProbability() {
    let totalProbability = 0.0

    for (let pair of this.elements) {
      totalProbability += pair.probabilityInput.probability()
    }

    return totalProbability
  }

  /**
   * Normalise the probabilities if each of the probabilities are valid.
   * @returns undefined
   */
  normalise() {
    // Calculate the total probability
    let p = this.totalProbability()

    // If the total probability is NaN (due to invalid probabilities) then
    // normalisation cannot be performed
    if (Number.isNaN(p)) {
      return
    }

    // Calculate the multiplier required to normalise each probability
    let multiplier = 1.0 / p

    // Adjust each of the probabilities
    for (let pair of this.elements) {
      pair.probabilityInput.stringValue *= multiplier
    }
  }

  /**
   * Checks the validity of the distribution.
   * @returns True if the discrete distribution is valid.
   */
  isValid() {
    // There must be at least one pair
    if (this.elements.length == 0) {
      return false
    }

    // All pairs must be valid
    let uniqueValues = new Set()
    for (let pair of this.elements) {
      if (!pair.isValid()) {
        return false
      }

      uniqueValues.add(pair.valueInput.value())
    }

    // The values in the pairs must be unique
    if (uniqueValues.size !== this.elements.length) {
      return false
    }

    // The probabilities of the pairs must sum to unity (within tolerance)
    return Math.abs(this.totalProbability() - 1.0) < 1e-6
  }

  /**
   * Checks if the elements of this distribution as within tolerance of the
   * otherElements.
   * @param {array} otherElements Array of (value, probability) pairs.
   * @returns True if the distributions are within tolerance.
   */
  equals(otherElements) {
    if (otherElements.length !== this.elements.length) {
      return false
    }

    for (let idx in this.elements) {
      let otherValue = otherElements[idx][0]
      let otherProbability = otherElements[idx][1]
      if (!this.elements[idx].equals(otherValue, otherProbability)) {
        return false
      }
    }

    return true
  }
}
