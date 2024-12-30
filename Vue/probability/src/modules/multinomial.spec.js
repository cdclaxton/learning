import { expect, test, describe } from 'vitest'
import { buildCdf, largestIndex, sampleMultinomialPMF } from './multinomial'

let distributionsEqual = (expected, actual) => {
  if (expected.length !== actual.length) {
    return false
  }

  for (let idx in expected) {
    if (Math.abs(expected[idx] - actual[idx]) > 1e-6) {
      return false
    }
  }

  return true
}

describe('buildCdf', () => {
  test('no probabilities', () => {
    expect(() => buildCdf([])).toThrowError('no probabilities')
  })

  test('probabilities do not sum to 1', () => {
    expect(() => buildCdf([0.3, 0.5])).toThrowError('probabilities do not sum to 1')
  })

  test('invalid probability', () => {
    expect(() => buildCdf([0.3, -0.3, 1.0])).toThrowError('invalid probability')
  })

  test('one probability', () => {
    let actual = buildCdf([1.0])
    let expected = [1.0]
    expect(distributionsEqual(actual, expected)).toBe(true)
  })

  test('two probabilities', () => {
    let actual = buildCdf([0.3, 0.7])
    let expected = [0.3, 1.0]
    expect(distributionsEqual(actual, expected)).toBe(true)
  })

  test('three probabilities', () => {
    let actual = buildCdf([0.3, 0.6, 0.1])
    let expected = [0.3, 0.9, 1.0]
    expect(distributionsEqual(actual, expected)).toBe(true)
  })
})

describe('largestIndex', () => {
  test('one value', () => {
    let u = Math.random()
    expect(largestIndex([1.0], u)).toBe(0)
  })

  test('two values', () => {
    expect(largestIndex([0.3, 1.0], 0.0)).toBe(0)
    expect(largestIndex([0.3, 1.0], 0.2)).toBe(0)
    expect(largestIndex([0.3, 1.0], 0.3)).toBe(0)
    expect(largestIndex([0.3, 1.0], 0.4)).toBe(1)
    expect(largestIndex([0.3, 1.0], 0.8)).toBe(1)
    expect(largestIndex([0.3, 1.0], 1.0)).toBe(1)
  })

  test('three values', () => {
    expect(largestIndex([0.3, 0.7, 1.0], 0.0)).toBe(0)
    expect(largestIndex([0.3, 0.7, 1.0], 0.2)).toBe(0)
    expect(largestIndex([0.3, 0.7, 1.0], 0.3)).toBe(0)
    expect(largestIndex([0.3, 0.7, 1.0], 0.4)).toBe(1)
    expect(largestIndex([0.3, 0.7, 1.0], 0.6)).toBe(1)
    expect(largestIndex([0.3, 0.7, 1.0], 0.7)).toBe(1)
    expect(largestIndex([0.3, 0.7, 1.0], 0.8)).toBe(2)
    expect(largestIndex([0.3, 0.7, 1.0], 1.0)).toBe(2)
  })
})

describe('sampleMultinomialPMF', () => {
  test('different number of values and probabilities', () => {
    expect(() => sampleMultinomialPMF([1.0, 2.0], [1.0], 1)).toThrowError(
      'inconsistent values and probabilities',
    )
  })

  test('invalid number of samples', () => {
    expect(() => sampleMultinomialPMF([1.0, 2.0], [0.4, 0.6], -1)).toThrowError(
      'invalid number of samples',
    )
  })

  test('one value', () => {
    let samples = sampleMultinomialPMF([5.0], [1.0], 10)
    expect(samples.length).toBe(10)

    for (let s of samples) {
      expect(s).toBe(5.0)
    }
  })

  test('two values', () => {
    let samples = sampleMultinomialPMF([5.0, 8.0], [0.3, 0.7], 10)
    expect(samples.length).toBe(10)

    let expectedValues = new Set([5.0, 8.0])
    for (let s of samples) {
      expect(expectedValues.has(s)).toBe(true)
    }
  })
})
