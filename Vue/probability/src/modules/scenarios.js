import { sampleMultinomialPMF } from './multinomial'

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

  toString() {
    return `${this.probability()}`
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

  toString() {
    return `${this.value()}`
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

  toString() {
    return `(v=${this.valueInput.toString()}, p=${this.probabilityInput.toString()})`
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

    // Don't normalise if the sum of the probabilities is zero
    if (p === 0) {
      return
    }

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

  /**
   * Draw n samples from the distribution.
   * @param {int} n Number of samples to draw.
   * @returns Array of samples.
   */
  sample(n) {
    if (!this.isValid()) {
      throw new Error('discrete distribution is invalid')
    }

    let values = this.elements.map((e) => e.valueInput.value())
    let probabilities = this.elements.map((e) => e.probabilityInput.probability())
    return sampleMultinomialPMF(values, probabilities, n)
  }

  toString() {
    let s = '['

    for (let i = 0; i < this.elements.length; i++) {
      s += this.elements[i].toString()
      if (i < this.elements.length - 1) {
        s += ', '
      }
    }

    return s + ']'
  }
}

export function dicreteDistributionFromSamples(samples) {
  if (samples.length === 0) {
    throw new Error('no samples from which to build a distribution')
  }

  // Number of samples
  let n = samples.length

  // Sort the samples in ascending order in place
  samples.sort((a, b) => a - b)

  let d = new DiscreteDistribution()

  let value = samples[0]
  let count = 1

  for (let i = 1; i < n; i++) {
    if (samples[i] === value) {
      count += 1
    } else {
      d.addElement(value, count / n)
      value = samples[i]
      count = 1
    }
  }

  d.addElement(value, count / n)

  // Return the populated distribution
  return d
}

export class Scenario {
  constructor() {
    this.name = ''
    this.distribution = new DiscreteDistribution()
    this.probabilityInput = new ProbabilityInput(0.0)
  }

  isValid() {
    return this.probabilityInput.isValid() && this.distribution.isValid()
  }

  normalise() {
    this.distribution.normalise()
  }

  addElement(value, probability) {
    this.distribution.addElement(value, probability)
  }

  deleteElement(idx) {
    return this.distribution.deleteElement(idx)
  }

  setProbability(p) {
    this.probabilityInput.stringValue = p
  }

  equals(otherName, otherDistribution) {
    return this.name === otherName && this.distribution.equals(otherDistribution)
  }

  /**
   * Generate n samples from the scenario.
   * @param {int} n Number of samples to generate.
   * @returns Array of samples (number or NaN).
   */
  sample(n) {
    if (!this.isValid()) {
      throw new Error('scenario is invalid')
    }

    // Generate n samples without censoring
    let samples = this.distribution.sample(n)

    // Probability that the scenario yields a value
    let p = this.probabilityInput.probability()

    // Apply censoring based on Bernoulli samples
    for (let i = 0; i < n; i++) {
      if (Math.random() > p) {
        samples[i] = NaN
      }
    }

    return samples
  }

  toString() {
    return `Name: ${this.name}, p: ${this.probabilityInput.probability()}, distribution: ${this.distribution.toString()}`
  }
}

export class Scenarios {
  constructor() {
    this.scenarios = []
    this.result = new DiscreteDistribution()
  }

  addScenario() {
    let s = new Scenario()
    this.scenarios.push(s)
  }

  deleteScenario(idx) {
    if (idx < 0 || idx >= this.scenarios.length) {
      return false
    }

    this.scenarios.splice(idx, 1)
    return true
  }

  clear() {
    this.scenarios = []
    this.result = new DiscreteDistribution()
  }

  /**
   * Check if all scenarios are valid.
   * @returns True if all scenarios are valid.
   */
  scenariosValid() {
    return this.scenarios.length > 0 && this.scenarios.every((s) => s.isValid())
  }

  calculate(n) {
    if (n === undefined || n < 1) {
      throw new Error(`invalid number of samples to generate: ${n}`)
    }

    if (!this.scenariosValid()) {
      return false
    }

    // Generate samples
    let samples = this.scenarios[0].sample(n)

    // Convert NaNs to 0s
    for (let i = 0; i < n; i++) {
      if (Number.isNaN(samples[i])) {
        samples[i] = 0
      }
    }

    for (let i = 1; i < this.scenarios.length; i++) {
      let scenarioSamples = this.scenarios[i].sample(n)
      for (let j = 0; j < n; j++) {
        if (!Number.isNaN(scenarioSamples[j])) {
          samples[j] = Math.max(samples[j], scenarioSamples[j])
        }
      }
    }

    // Convert the samples to a distribution
    this.result = dicreteDistributionFromSamples(samples)

    return true
  }

  toString() {
    let s = 'scenarios = ['

    for (let i = 0; i < this.scenarios.length; i++) {
      s += this.scenarios[i].toString()
      if (i < this.scenarios.length - 1) {
        s += ', '
      }
    }

    return s + '], result = ' + this.result.toString()
  }
}

export function exampleScenarios(nSamplesForCalculation) {
  let s = new Scenarios()

  // Add the first scenario
  s.addScenario()
  s.scenarios[0].name = 'Outcome 1'
  s.scenarios[0].setProbability(0.8)
  s.scenarios[0].addElement(2.0, 0.5)
  s.scenarios[0].addElement(3.0, 0.2)
  s.scenarios[0].addElement(5.0, 0.3)

  // Add the second scenario
  s.addScenario()
  s.scenarios[1].name = 'Outcome 2'
  s.scenarios[1].setProbability(0.3)
  s.scenarios[1].addElement(3.0, 0.9)
  s.scenarios[1].addElement(10.0, 0.1)

  s.calculate(nSamplesForCalculation)

  return s
}
