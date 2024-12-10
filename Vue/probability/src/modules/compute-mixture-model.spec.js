import { expect, test, describe } from 'vitest'
import { mixtureModel, MixtureModelInput } from './compute-mixture-model'
import { Distribution } from './probability'
import exp from 'constants'

describe('mixture model', () => {
  test('no inputs', () => {
    expect(() => mixtureModel()).toThrowError('no inputs')
  })

  test('one input, prob = 1', () => {
    let dist = new Distribution([0, 1], [0.2, 0.8])
    let input = new MixtureModelInput(dist, 1.0)
    expect(mixtureModel(input).equals(dist, 1e-5).success).toBe(true)
  })

  test('one input, prob != 1', () => {
    let dist = new Distribution([0, 1], [0.2, 0.8])
    let input = new MixtureModelInput(dist, 0.2)
    expect(() => mixtureModel(input)).toThrowError('probability of single input is not 1')
  })

  test('two inputs', () => {
    let dist1 = new Distribution([0, 1], [0.2, 0.8])
    let dist2 = new Distribution([1, 2], [0.6, 0.4])

    expect(
      mixtureModel(new MixtureModelInput(dist1, 1.0), new MixtureModelInput(dist2, 0.0)).equals(
        dist1,
      ).success,
    ).toBe(true)

    expect(
      mixtureModel(new MixtureModelInput(dist1, 0.0), new MixtureModelInput(dist2, 1.0)).equals(
        dist2,
      ).success,
    ).toBe(true)
  })
})
