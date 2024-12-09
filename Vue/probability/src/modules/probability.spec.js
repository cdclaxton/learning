import { expect, test, describe } from 'vitest'
import {
  hasUniqueValues,
  ProbabilityElement,
  probabilitiesValid,
  Distribution,
  valuesEqual,
  probabilitiesInTolerance,
  distributionsInTolerance,
} from './probability'

describe('ProbabilityElement', () => {
  test('valid value and probability', () => {
    let element = new ProbabilityElement(10.4, 0.8)
    expect(element.value).toBe(10.4)
    expect(element.probability).toBe(0.8)
  })

  test('invalid probability', () => {
    expect(() => new ProbabilityElement(10.0, -0.1)).toThrowError('invalid probability')
  })
})

describe('hasUniqueValues', () => {
  test('no duplicates', () => {
    expect(hasUniqueValues([1])).toBe(true)
    expect(hasUniqueValues([1, 2])).toBe(true)
    expect(hasUniqueValues([10, 20, 30])).toBe(true)
  })

  test('duplicate values', () => {
    expect(hasUniqueValues([2, 2])).toBe(false)
    expect(hasUniqueValues([10, 20, 10])).toBe(false)
  })
})

describe('probabilitiesValid', () => {
  test('probabilities sum to 1', () => {
    expect(probabilitiesValid([1.0])).toBe(true)
    expect(probabilitiesValid([0.3, 0.7])).toBe(true)
  })

  test('probability out of range', () => {
    expect(probabilitiesValid([-0.1])).toBe(false)
    expect(probabilitiesValid([1.1])).toBe(false)
  })

  test('probabilities do not sum to 1', () => {
    expect(probabilitiesValid([0.2, 0.8, 0.1])).toBe(false)
  })
})

describe('Distribution', () => {
  test('empty values and probabilities', () => {
    expect(() => new Distribution([], [])).toThrowError('no values')
  })

  test('inconsistent values and probabilities', () => {
    expect(() => new Distribution([2, 3], [1.0])).toThrowError(
      'values and probabilities have differing lengths',
    )
  })

  test('duplicate values', () => {
    expect(() => new Distribution([1, 2, 1], [0.4, 0.5, 0.1])).toThrowError('values are not unique')
  })

  test('invalid probabilities', () => {
    expect(() => new Distribution([1, 2], [0.9, 0.2]).toThrowError('invalid probabilities'))
    expect(() => new Distribution([1, 2], [1.1, 0.0]).toThrowError('invalid probabilities'))
  })

  test('valid values and probabilities', () => {
    let dist = new Distribution([1, 2, 3], [0.2, 0.5, 0.3])
    expect(dist.values).toStrictEqual([1, 2, 3])
    expect(dist.probabilities).toStrictEqual([0.2, 0.5, 0.3])
  })
})

describe('valuesEqual', () => {
  test('equal values', () => {
    expect(valuesEqual([1], [1])).toBe(true)
    expect(valuesEqual([1, 2], [1, 2])).toBe(true)
    expect(valuesEqual([10, 20, 30], [10, 20, 30])).toBe(true)
  })

  test('values not equal', () => {
    expect(valuesEqual([], [2])).toBe(false)
    expect(valuesEqual([1], [])).toBe(false)
    expect(valuesEqual([1], [2])).toBe(false)
    expect(valuesEqual([1, 2], [2, 1])).toBe(false)
    expect(valuesEqual([1, 2, 3], [1, 2])).toBe(false)
  })
})

describe('probabilitiesInTolerance', () => {
  let tol = 1e-4
  test('differing lengths', () => {
    expect(probabilitiesInTolerance([], [0.2, 0.8], tol)).toBe(false)
    expect(probabilitiesInTolerance([1.0], [0.2, 0.8], tol)).toBe(false)
  })

  test('same length, different values', () => {
    expect(probabilitiesInTolerance([0.9, 0.1], [0.2, 0.8], tol)).toBe(false)
    expect(probabilitiesInTolerance([0.85, 0.15], [0.9, 0.1], tol)).toBe(false)
  })

  test('same length, same values', () => {
    expect(probabilitiesInTolerance([1.0], [1.0], tol)).toBe(true)
    expect(probabilitiesInTolerance([0.1, 0.9], [0.1, 0.9], tol)).toBe(true)
    expect(probabilitiesInTolerance([0.1, 0.8, 0.1], [0.1, 0.8, 0.1], tol)).toBe(true)
  })
})

describe('distributionsInTolerance', () => {
  let tolerance = 1e-5
  let dist1 = new Distribution([0], [1.0])
  let dist2 = new Distribution([0, 1], [0.2, 0.8])

  test('invalid tolerance', () => {
    expect(() => distributionsInTolerance(dist1, dist1, -1.0)).toThrowError('tolerance is invalid')
  })

  test('distributions identical', () => {
    expect(distributionsInTolerance(dist1, dist1, tolerance).success).toBe(true)
    expect(distributionsInTolerance(dist2, dist2, tolerance).success).toBe(true)
  })

  test('distributions of differing lengths', () => {
    expect(distributionsInTolerance(dist1, dist2, tolerance).success).toBe(false)
  })
})

describe('Distributions equal', () => {
  let tolerance = 1e-5
  let dist1 = new Distribution([0], [1.0])
  let dist2 = new Distribution([0, 1], [0.2, 0.8])

  test('identical distributions', () => {
    expect(dist1.equals(dist1, tolerance).success).toBe(true)
    expect(dist2.equals(dist2, tolerance).success).toBe(true)
  })

  test('distributions differ', () => {
    expect(dist1.equals(dist2, tolerance).success).toBe(false)
  })
})
