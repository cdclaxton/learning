import { Distribution } from './probability'

/**
 * Converts an object (e.g. {0.5:0.2, 2:0.8}) to a Distribution.
 * @param {Object} obj
 * @returns
 */
export function objectToDistribution(obj) {
  let keys = Object.keys(obj)
    .map(Number)
    .sort((a, b) => a - b)
  let values = []
  let probabilities = []

  for (let k of keys) {
    values.push(k)
    probabilities.push(obj[k])
  }

  return new Distribution(values, probabilities)
}

/**
 * Calculate the distribution of the sum of one or more distributions.
 * @param  {...Distribution} dists Distributions
 * @returns {Distribution}
 */
export function addDistributions(...dists) {
  if (dists.length == 0) {
    throw new Error('no distributions')
  }

  if (dists.length == 1) {
    return dists[0]
  } else if (dists.length > 2) {
    let a, rest
    ;[a, ...rest] = dists
    return addDistributions(a, addDistributions(...rest))
  }

  // At this point there will be just two distributions
  let a, rest
  ;[a, ...rest] = dists
  let b = rest[0]

  let result = {}
  for (let ai in a.values) {
    for (let bi in b.values) {
      let element = a.values[ai] + b.values[bi]
      let prob = a.probabilities[ai] * b.probabilities[bi]

      if (!(element in result)) {
        result[element] = prob
      } else {
        result[element] += prob
      }
    }
  }

  return objectToDistribution(result)
}
