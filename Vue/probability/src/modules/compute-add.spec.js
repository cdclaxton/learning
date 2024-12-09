import { expect, test, describe } from 'vitest'
import { Distribution } from './probability'
import { addDistributions, objectToDistribution } from './compute-add'

describe('objectToDistribution', () => {
  test('distribution with one value', () => {
    expect(
      objectToDistribution({ 0.5: 1.0 }).equals(new Distribution([0.5], [1.0]), 1e-3).success,
    ).toBe(true)
  })

  test('distribution with two values', () => {
    expect(
      objectToDistribution({ 0.5: 0.2, 2: 0.8 }).equals(
        new Distribution([0.5, 2.0], [0.2, 0.8]),
        1e-3,
      ).success,
    ).toBe(true)
  })

  test('distribution with three values', () => {
    expect(
      objectToDistribution({ 0.5: 0.2, 2: 0.3, 4: 0.5 }).equals(
        new Distribution([0.5, 2.0, 4.0], [0.2, 0.3, 0.5]),
        1e-3,
      ).success,
    ).toBe(true)
  })
})

describe('sum of two distributions', () => {
  let tolerance = 1e-5

  test('no distributions', () => {
    expect(() => addDistributions()).toThrowError('no distributions')
  })

  test('one distribution', () => {
    let dist1 = new Distribution([0.5, 3], [0.2, 0.8])
    expect(addDistributions(dist1).equals(dist1, tolerance).success).toBe(true)
  })

  test('distributions of zeros', () => {
    let dist1 = new Distribution([0], [1.0])
    expect(addDistributions(dist1).equals(dist1, tolerance).success).toBe(true)
    expect(addDistributions(dist1, dist1).equals(dist1, tolerance).success).toBe(true)
    expect(addDistributions(dist1, dist1, dist1).equals(dist1, tolerance).success).toBe(true)
  })

  test('distributions with all mass on one value', () => {
    let dist1 = new Distribution([1], [1.0])
    let dist2 = new Distribution([2], [1.0])
    expect(addDistributions(dist1, dist2).equals(new Distribution([3], [1.0])).success).toBe(true)
  })

  test('two distributions', () => {
    let dist1 = new Distribution([1, 2], [0.2, 0.8])
    let dist2 = new Distribution([1, 5], [0.8, 0.2])
    // 1+1 = 2, prob = 0.2*0.8
    // 1+5 = 6, prob = 0.2*0.2
    // 2+1 = 3, prob = 0.8*0.8
    // 2+5 = 7, prob = 0.8*0.2
    let expected = new Distribution([2, 3, 6, 7], [0.2 * 0.8, 0.8 * 0.8, 0.2 * 0.2, 0.8 * 0.2])
    expect(addDistributions(dist1, dist2).equals(expected).success).toBe(true)
  })
})
