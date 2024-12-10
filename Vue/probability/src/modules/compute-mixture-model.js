import { objectToDistribution } from './compute-basic'

/**
 * Mixture model input.
 */
export class MixtureModelInput {
  constructor(dist, probability) {
    this.dist = dist
    this.probability = probability
  }
}

export function mixtureModel(...inputs) {
  if (inputs.length === 0) {
    throw new Error('no inputs')
  } else if (inputs.length === 1) {
    if (inputs[0].probability !== 1.0) {
      throw new Error('probability of single input is not 1')
    }
    return inputs[0].dist
  }

  // There are two or more inputs at this point
  let result = {}
  let totalProbability = 0.0

  for (let i of inputs) {
    totalProbability += i.probability

    for (let idx in i.dist.values) {
      let element = i.dist.values[idx]
      let prob = i.dist.probabilities[idx] * i.probability

      if (prob === 0) {
        continue
      }

      if (!(element in result)) {
        result[element] = prob
      } else {
        result[element] += prob
      }
    }
  }

  if (Math.abs(totalProbability - 1.0) > 1e-6) {
    throw new Error(`probability of inputs does not sum to 1 (${totalProbability}`)
  }

  return objectToDistribution(result)
}
