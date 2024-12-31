import { expect, test, describe } from 'vitest'
import {
  DistributionElement,
  DiscreteDistribution,
  ProbabilityInput,
  ValueInput,
  Scenario,
  Scenarios,
  dicreteDistributionFromSamples,
} from './scenarios'

let invalidProbability = (p) => Number.isNaN(p.probability())

describe('ProbabilityInput', () => {
  test('empty value', () => {
    let p = new ProbabilityInput('')
    expect(p.isValid()).toBe(false)
    expect(invalidProbability(p)).toBe(true)
    expect(p.equals(NaN)).toBe(true)
  })

  test('letters', () => {
    let p = new ProbabilityInput('abc')
    expect(p.isValid()).toBe(false)
    expect(invalidProbability(p)).toBe(true)
    expect(p.equals(NaN)).toBe(true)
  })

  test('negative value', () => {
    let p = new ProbabilityInput('-1.0')
    expect(p.isValid()).toBe(false)
    expect(invalidProbability(p)).toBe(true)
    expect(p.equals(NaN)).toBe(true)
  })

  test('number > 1', () => {
    let p = new ProbabilityInput('1.1')
    expect(p.isValid()).toBe(false)
    expect(invalidProbability(p)).toBe(true)
    expect(p.equals(NaN)).toBe(true)
  })

  test('probability = 0.0', () => {
    let p = new ProbabilityInput('0.0')
    expect(p.isValid()).toBe(true)
    expect(invalidProbability(p)).toBe(false)
    expect(p.equals(0.0)).toBe(true)
  })

  test('probability = 1.0', () => {
    let p = new ProbabilityInput('1.0')
    expect(p.isValid()).toBe(true)
    expect(invalidProbability(p)).toBe(false)
    expect(p.equals(1.0)).toBe(true)
  })

  test('valid probability', () => {
    for (let i = 0; i < 10; i++) {
      let n = Math.random()
      let p = new ProbabilityInput('' + n)
      expect(p.isValid()).toBe(true)
      expect(p.probability()).toBe(n)
      expect(p.equals(n)).toBe(true)
    }
  })

  test('set probability', () => {
    let p = new ProbabilityInput('')
    p.stringValue = '0.4'
    expect(p.isValid()).toBe(true)
    expect(p.probability()).toBe(0.4)
    expect(p.equals(0.4)).toBe(true)
  })
})

describe('ValueInput', () => {
  test('empty value', () => {
    let v = new ValueInput('')
    expect(v.isValid()).toBe(false)
    expect(Number.isNaN(v.value())).toBe(true)
    expect(v.equals(NaN)).toBe(true)
  })

  test('letters', () => {
    let v = new ValueInput('')
    expect(v.isValid()).toBe(false)
    expect(Number.isNaN(v.value())).toBe(true)
    expect(v.equals(NaN)).toBe(true)
  })

  test('valid value', () => {
    let n = Math.random() * 2 - 1
    let v = new ValueInput('' + n)
    expect(v.isValid()).toBe(true)
    expect(v.value()).toBe(n)
    expect(v.equals(n)).toBe(true)
  })
})

describe('DistributionElement', () => {
  test('valid value, invalid probability', () => {
    let e = new DistributionElement(1.0, 'c')
    expect(e.isValid()).toBe(false)
    expect(e.equals(1.0, NaN)).toBe(true)
  })

  test('invalid value, valid probability', () => {
    let e = new DistributionElement('c', 0.4)
    expect(e.isValid()).toBe(false)
    expect(e.equals(NaN, 0.4)).toBe(true)
  })

  test('valid value, valid probability', () => {
    let e = new DistributionElement(2.0, 0.4)
    expect(e.isValid()).toBe(true)
    expect(e.equals(2.0, 0.4)).toBe(true)
  })
})

describe('DiscreteDistribution.equals', () => {
  test('no elements', () => {
    let d = new DiscreteDistribution()
    expect(d.equals([])).toBe(true)
  })

  test('one element', () => {
    let d = new DiscreteDistribution()
    d.addElement(2.0, 0.5)
    expect(d.equals([[2.0, 0.5]])).toBe(true)
  })

  test('two elements', () => {
    let d = new DiscreteDistribution()
    d.addElement(2.0, 0.7)
    d.addElement(4.0, 0.3)
    expect(
      d.equals([
        [2.0, 0.7],
        [4.0, 0.3],
      ]),
    ).toBe(true)
  })
})

describe('DiscreteDistribution.totalProbability', () => {
  test('empty distribution', () => {
    let d = new DiscreteDistribution()
    expect(d.totalProbability()).toBe(0)
  })

  test('single element', () => {
    let p = Math.random()
    let d = new DiscreteDistribution({ 1: p })
    expect(d.totalProbability()).toBe(p)
  })

  test('two elements', () => {
    let p1 = Math.random() / 2
    let p2 = Math.random() / 2
    let d = new DiscreteDistribution({ 1: p1, 3: p2 })
    expect(d.totalProbability()).toBeCloseTo(p1 + p2, 10)
  })

  test('invalid probability', () => {
    let d = new DiscreteDistribution({ 2: 'c' })
    expect(d.totalProbability()).toBeNaN()
  })
})

describe('DiscreteDistribution.normalise', () => {
  test('no values', () => {
    let d = new DiscreteDistribution()
    d.normalise()
    expect(d.elements.length).toBe(0)
  })

  test('one value, normalised', () => {
    let d = new DiscreteDistribution({ 2: 1.0 })
    d.normalise()
    expect(d.equals([[2, 1.0]])).toBe(true)
  })

  test('one value = 0', () => {
    let d = new DiscreteDistribution({ 2: 0.0 })
    d.normalise()
    expect(d.equals([[2, 0.0]])).toBe(true)
  })

  test('two values, normalised', () => {
    let d = new DiscreteDistribution()
    d.addElement(1, 0.3)
    d.addElement(3, 0.7)
    d.normalise()
    expect(
      d.equals([
        [1, 0.3],
        [3, 0.7],
      ]),
    ).toBe(true)
  })

  test('one value, unnormalised', () => {
    let d = new DiscreteDistribution({ 2: 0.2 })
    d.normalise()
    expect(d.equals([[2, 1.0]])).toBe(true)
  })

  test('two values, unnormalised', () => {
    let d = new DiscreteDistribution()
    d.addElement(1, 0.2)
    d.addElement(3, 0.3)
    d.normalise()
    expect(
      d.equals([
        [1, 0.4],
        [3, 0.6],
      ]),
    ).toBe(true)
  })
})

describe('DiscreteDistribution.isValid', () => {
  test('no elements', () => {
    let d = new DiscreteDistribution()
    expect(d.isValid()).toBe(false)
  })

  test('one element, probability != 1', () => {
    let d = new DiscreteDistribution({ 1: 0.8 })
    expect(d.isValid()).toBe(false)
  })

  test('one element, probability == 1', () => {
    let d = new DiscreteDistribution({ 1: 1.0 })
    expect(d.isValid()).toBe(true)
  })

  test('one element, invalid probability', () => {
    let d = new DiscreteDistribution({ 1: 'c' })
    expect(d.isValid()).toBe(false)
  })

  test('two elements, valid', () => {
    let d = new DiscreteDistribution()
    d.addElement(2, 0.3)
    d.addElement(3, 0.7)
    expect(d.isValid()).toBe(true)
  })

  test('two elements, probability sum != 1', () => {
    let d = new DiscreteDistribution()
    d.addElement(2, 0.3)
    d.addElement(3, 0.6)
    expect(d.isValid()).toBe(false)
  })

  test('two elements, duplicate values', () => {
    let d = new DiscreteDistribution()
    d.addElement(2, 0.3)
    d.addElement(2, 0.7)
    expect(d.isValid()).toBe(false)
  })
})

describe('DiscreteDistribution.deleteElement', () => {
  test('one element', () => {
    let d = new DiscreteDistribution()
    d.addElement(10, 1.0)
    expect(d.equals([[10, 1.0]])).toBe(true)
    expect(d.deleteElement(1)).toBe(false)
    expect(d.deleteElement(0)).toBe(true)
    expect(d.equals([])).toBe(true)
  })

  test('two elements', () => {
    let d = new DiscreteDistribution()
    d.addElement(10, 0.4)
    d.addElement(20, 0.6)
    expect(
      d.equals([
        [10, 0.4],
        [20, 0.6],
      ]),
    ).toBe(true)
    expect(d.deleteElement(-1)).toBe(false)
    expect(d.deleteElement(0)).toBe(true)
    expect(d.equals([[20, 0.6]])).toBe(true)
  })
})

describe('DiscreteDistribution.sample', () => {
  test('one element', () => {
    let d = new DiscreteDistribution()
    d.addElement(5.0, 1.0)
    let samples = d.sample(10)
    expect(samples.length).toBe(10)
  })

  test('two elements', () => {
    let d = new DiscreteDistribution()
    d.addElement(5.0, 0.5)
    d.addElement(8.0, 0.5)

    let samples = d.sample(10)
    expect(samples.length).toBe(10)

    let expectedValues = new Set([5.0, 8.0])
    for (let s of samples) {
      expect(expectedValues.has(s)).toBe(true)
    }
  })
})

describe('Scenario.sample', () => {
  test('scenario probability == 0', () => {
    let scenario = new Scenario()
    scenario.addElement(2.0, 1.0)
    scenario.setProbability(0.0)
    let samples = scenario.sample(10)
    expect(samples.length).toBe(10)

    for (let s of samples) {
      expect(Number.isNaN(s)).toBe(true)
    }
  })

  test('scenario probability == 1', () => {
    let scenario = new Scenario()
    scenario.addElement(2.0, 1.0)
    scenario.setProbability(1.0)
    let samples = scenario.sample(10)
    expect(samples.length).toBe(10)

    for (let s of samples) {
      expect(s === 2.0).toBe(true)
    }
  })
})

describe('dicreteDistributionFromSamples', () => {
  test('no samples', () => {
    expect(() => dicreteDistributionFromSamples([])).toThrowError(
      'no samples from which to build a distribution',
    )
  })

  test('one sample', () => {
    let d = dicreteDistributionFromSamples([2.0])
    expect(d.equals([[2.0, 1.0]])).toBe(true)
  })

  test('two samples (same)', () => {
    let d = dicreteDistributionFromSamples([3.0, 3.0])
    expect(d.equals([[3.0, 1.0]])).toBe(true)
  })

  test('two samples (different)', () => {
    let d = dicreteDistributionFromSamples([3.0, 5.0])
    expect(
      d.equals([
        [3.0, 0.5],
        [5.0, 0.5],
      ]),
    ).toBe(true)
  })

  test('three samples', () => {
    let d = dicreteDistributionFromSamples([3.0, 5.0, 3.0])
    expect(
      d.equals([
        [3.0, 2 / 3],
        [5.0, 1 / 3],
      ]),
    ).toBe(true)
  })
})

describe('Scenarios.calculate', () => {
  test('invalid number of samples', () => {
    let s = new Scenarios()
    expect(() => s.calculate(-1)).toThrowError('invalid number of samples to generate')
  })

  test('no scenarios', () => {
    let s = new Scenarios()
    expect(s.calculate(10)).toBe(false)
  })

  test('one scenario, p=0', () => {
    let s = new Scenarios()
    s.addScenario()
    s.scenarios[0].addElement(5.0, 1.0)
    s.scenarios[0].setProbability(0)
    expect(s.scenarios.length).toBe(1)
    expect(s.calculate(10)).toBe(true)
    expect(s.result.equals([[0.0, 1.0]])).toBe(true)
  })

  test('one scenario, p=1', () => {
    let s = new Scenarios()
    s.addScenario()
    s.scenarios[0].addElement(5.0, 1.0)
    s.scenarios[0].setProbability(1)
    expect(s.scenarios.length).toBe(1)
    expect(s.calculate(10)).toBe(true)
    expect(s.result.equals([[5.0, 1.0]])).toBe(true)
  })
})
