import { expect, test, describe } from 'vitest'
import {
  randomInteger,
  Question,
  Answer,
  QuestionAnswer,
  additionQuestionGenerator,
  questionGenerator,
  Operator,
  subtractionQuestionGenerator,
  multiplicationQuestionGenerator,
  divisionQuestionGenerator,
  generateListQuestions,
  QuestionSet,
} from './question'

describe('Question', () => {
  test('addition', () => {
    for (let i = 0; i < 100; i++) {
      const n1 = randomInteger(0, 10)
      const n2 = randomInteger(0, 20)
      const q = new Question(n1, n2, '+')
      expect(q.expected()).toBe(n1 + n2)
    }
  })

  test('subtraction', () => {
    for (let i = 0; i < 100; i++) {
      const n1 = randomInteger(0, 10)
      const n2 = randomInteger(0, 20)
      const q = new Question(n1, n2, '-')
      expect(q.expected()).toBe(n1 - n2)
    }
  })

  test('multiplication', () => {
    for (let i = 0; i < 100; i++) {
      const n1 = randomInteger(0, 10)
      const n2 = randomInteger(0, 20)
      const q = new Question(n1, n2, '*')
      expect(q.expected()).toBe(n1 * n2)
    }
  })

  test('division', () => {
    for (let i = 0; i < 100; i++) {
      const r = randomInteger(1, 10)
      const n2 = randomInteger(1, 20)

      //    n1 / n2 = r
      // => n1 = r n2
      const n1 = r * n2

      const q = new Question(n1, n2, '/')
      expect(q.expected()).toBe(r)
    }
  })
})

describe('Answer', () => {
  test('empty', () => {
    const a = new Answer()
    expect(a.parse()).toBe(null)
  })

  test('not a number', () => {
    const a = new Answer()
    a.stringValue = 'a1'
    expect(a.parse()).toBe(null)
  })

  test('number', () => {
    const a = new Answer()
    for (let i = 0; i < 100; i++) {
      const v = randomInteger(0, 100)
      a.stringValue = String(v)
      expect(a.parse()).toBe(v)
    }
  })
})

describe('QuestionAnswer', () => {
  test('empty answer', () => {
    const qa = new QuestionAnswer(1, 2, '+')
    expect(qa.isAnswered()).toBe(false)
    expect(qa.isCorrectAnswer()).toBe(false)
  })

  test('answer is not a number', () => {
    const qa = new QuestionAnswer(1, 2, '+')
    qa.answer.stringValue = 'c'
    expect(qa.isAnswered()).toBe(true)
    expect(qa.isCorrectAnswer()).toBe(false)
  })

  test('answer is incorrect', () => {
    const qa = new QuestionAnswer(1, 2, '+')
    qa.answer.stringValue = '4'
    expect(qa.isAnswered()).toBe(true)
    expect(qa.isCorrectAnswer()).toBe(false)
  })

  test('answer is correct', () => {
    const qa = new QuestionAnswer(1, 2, '+')
    qa.answer.stringValue = '3'
    expect(qa.isAnswered()).toBe(true)
    expect(qa.isCorrectAnswer()).toBe(true)
  })
})

type questionConstraint = (q: Question) => boolean

let constraintDiffPositiveOrZero: questionConstraint = (q: Question) => {
  return q.n1 - q.n2 >= 0
}

let constraintIntegerRatio: questionConstraint = (q: Question) => {
  return Number.isInteger(q.n1 / q.n2)
}

let questionTester = (
  generatorMinValue: number,
  generatorMaxValue: number,
  n1Range: [number, number],
  n2Range: [number, number],
  gen: questionGenerator,
  expectedOperator: Operator,
  constraint: questionConstraint | undefined = undefined,
) => {
  const q = gen(generatorMinValue, generatorMaxValue)

  // Check the question's numbers
  expect(
    n1Range[0] <= q.n1 && q.n1 <= n1Range[1],
    `expected n1 in range [${n1Range[0]}, ${n1Range[1]}], but got ${q.n1}`,
  ).toBe(true)

  expect(
    n2Range[0] <= q.n2 && q.n2 <= n2Range[1],
    `expected n2 in range [${n2Range[0]}, ${n2Range[1]}], but got ${q.n2}`,
  ).toBe(true)

  // Check the operator
  expect(q.op).toBe(expectedOperator)

  // Check the constraint (if applicable)
  if (constraint !== undefined) {
    expect(constraint(q), `constaint failed with n1=${q.n1}, n2=${q.n2}`).toBe(true)
  }
}

describe('question generators', () => {
  test('addition', () => {
    for (let i = 0; i < 100; i++) {
      questionTester(1, 10, [1, 10], [1, 10], additionQuestionGenerator, '+')
    }
  })

  test('subtraction', () => {
    for (let i = 0; i < 100; i++) {
      questionTester(
        1,
        10,
        [1, 10],
        [1, 10],
        subtractionQuestionGenerator,
        '-',
        constraintDiffPositiveOrZero,
      )
    }
  })

  test('multiplication', () => {
    for (let i = 0; i < 100; i++) {
      questionTester(1, 10, [1, 10], [1, 10], multiplicationQuestionGenerator, '*')
    }
  })

  test('division', () => {
    for (let i = 0; i < 100; i++) {
      questionTester(
        1,
        10,
        [1, 100],
        [1, 10],
        divisionQuestionGenerator,
        '/',
        constraintIntegerRatio,
      )
    }
  })
})

describe('generateListQuestions', () => {
  test('generate', () => {
    const qs = generateListQuestions(10, 1, 20)
    expect(qs.length).toBe(10)
  })
})

describe('QuestionSet', () => {
  test('percentage complete', () => {
    const qas = [new QuestionAnswer(2, 3, '+'), new QuestionAnswer(5, 6, '*')]
    const qSet = new QuestionSet(qas)

    // No questions answered
    expect(qSet.percentageComplete()).toBe(0)

    // First question answered incorrectly
    qSet.questionAnswers[0].answer.stringValue = '4'
    expect(qSet.percentageComplete()).toBe(0)

    // First question answered correctly
    qSet.questionAnswers[0].answer.stringValue = '5'
    expect(qSet.percentageComplete()).toBe(50)

    // Second question answered correctly
    qSet.questionAnswers[1].answer.stringValue = '30'
    expect(qSet.percentageComplete()).toBe(100)

    // Second question answered incorrectly
    qSet.questionAnswers[1].answer.stringValue = '19'
    expect(qSet.percentageComplete()).toBe(50)
  })
})
