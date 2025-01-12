/**
 * Mathematical operator in a question.
 */
export type Operator = '+' | '-' | '*' | '/'

/**
 * Returns a random integer in the range [min, max].
 * @param min Minimum value.
 * @param max Maximum value.
 * @returns Random integer.
 */
export function randomInteger(min: number, max: number): number {
  min = Math.ceil(min)
  max = Math.floor(max)
  return Math.floor(Math.random() * (max - min + 1)) + min
}

/**
 * Returns a pair of random numbers, where each value is in the range [min, max].
 * @param min Minimum value.
 * @param max Maximum value.
 * @returns Tuple of random numbers.
 */
export function pairOfRandomIntegers(min: number, max: number): [number, number] {
  return [randomInteger(min, max), randomInteger(min, max)]
}

/**
 * Question composed of two numbers (integers) and a mathematical operator.
 */
export class Question {
  constructor(
    readonly n1: number,
    readonly n2: number,
    readonly op: Operator,
  ) {}

  expected(): number {
    if (this.op === '+') {
      return this.n1 + this.n2
    } else if (this.op === '-') {
      return this.n1 - this.n2
    } else if (this.op === '*') {
      return this.n1 * this.n2
    } else if (this.op === '/') {
      return Math.round(this.n1 / this.n2)
    }

    throw Error(`Unknown operation: '${this.op}'`)
  }
}

/**
 * Answer with a stringValue for binding to a text box.
 */
export class Answer {
  stringValue: string = ''

  parse(): number | null {
    const v = parseFloat(this.stringValue)
    if (Number.isNaN(v)) {
      return null
    }

    if (!Number.isInteger(v)) {
      return null
    }

    return Math.round(v)
  }
}

/**
 * QuestionAnswer is a pair of a Question and its Answer.
 */
export class QuestionAnswer {
  question: Question
  answer: Answer

  constructor(n1: number, n2: number, op: Operator) {
    this.question = new Question(n1, n2, op)
    this.answer = new Answer()
  }

  /**
   * Has the question been answered?
   * @returns True if the question has been answered.
   */
  isAnswered(): boolean {
    return this.answer.stringValue.length > 0
  }

  /**
   * Is the answer correct?
   * @returns True if the answer is correct.
   */
  isCorrectAnswer(): boolean {
    const parsedAnswer = this.answer.parse()
    if (parsedAnswer === null) {
      return false
    }

    return parsedAnswer === this.question.expected()
  }

  static fromQuestion(q: Question): QuestionAnswer {
    return new QuestionAnswer(q.n1, q.n2, q.op)
  }
}

/**
 * Question generator function type
 */
export type questionGenerator = (minValue: number, maxValue: number) => Question

/**
 * Generate an addition question.
 * @param minValue Minimum value of each of the numbers.
 * @param maxValue Maximum value of each of the numbers.
 * @returns Addition question.
 */
export const additionQuestionGenerator: questionGenerator = (minValue, maxValue) => {
  const [n1, n2] = pairOfRandomIntegers(minValue, maxValue)
  return new Question(n1, n2, '+')
}

/**
 * Generate a subtraction question.
 * @param minValue Minimum value of each of the numbers.
 * @param maxValue Maximum value of each of the numbers.
 * @returns Subtraction question.
 */
export const subtractionQuestionGenerator: questionGenerator = (minValue, maxValue) => {
  let [n1, n2] = pairOfRandomIntegers(minValue, maxValue)

  while (n1 - n2 < 0) {
    ;[n1, n2] = pairOfRandomIntegers(minValue, maxValue)
  }

  return new Question(n1, n2, '-')
}

/**
 * Generate a multiplication question.
 * @param minValue Minimum value of each of the numbers.
 * @param maxValue Maximum value of each of the numbers.
 * @returns Multiplication question.
 */
export const multiplicationQuestionGenerator: questionGenerator = (minValue, maxValue) => {
  const [n1, n2] = pairOfRandomIntegers(minValue, maxValue)
  return new Question(n1, n2, '*')
}

/**
 * Generate a division question.
 * @param minValue Minimum value of the first number and answer.
 * @param maxValue Maximum value of the first number and answer.
 * @returns Division question.
 */
export const divisionQuestionGenerator: questionGenerator = (minValue, maxValue) => {
  const [r, n2] = pairOfRandomIntegers(minValue, maxValue)
  const n1 = r * n2
  return new Question(n1, n2, '/')
}

type listOfQuestions = QuestionAnswer[]

export const generateListQuestions = (
  n: number,
  minValue: number,
  maxValue: number,
): listOfQuestions => {
  const questions: listOfQuestions = []

  const fns: questionGenerator[] = [
    additionQuestionGenerator,
    subtractionQuestionGenerator,
    multiplicationQuestionGenerator,
    divisionQuestionGenerator,
  ]

  for (let i = 0; i < n; i++) {
    // Randomly select a question type
    const questionType = randomInteger(0, 3)
    const q: Question = fns[questionType](minValue, maxValue)
    questions.push(QuestionAnswer.fromQuestion(q))
  }

  return questions
}

export class QuestionSet {
  constructor(public questionAnswers: QuestionAnswer[]) {}

  percentageComplete(): number {
    const totalCorrect = this.questionAnswers
      .map((qa) => qa.isAnswered() && qa.isCorrectAnswer())
      .filter((v) => v).length
    return Math.round((100 * totalCorrect) / this.questionAnswers.length)
  }
}
