<script lang="ts">
import { QuestionAnswer } from '../modules/question'

export default {
  props: {
    qa: QuestionAnswer,
  },
  methods: {
    answeredAndCorrect() {
      return this.qa.isAnswered() && this.qa.isCorrectAnswer()
    },
    operation() {
      if (this.qa.question.op === '+') {
        return '&plus;'
      } else if (this.qa.question.op === '-') {
        return '&minus;'
      } else if (this.qa.question.op === '*') {
        return '&times;'
      } else if (this.qa.question.op === '/') {
        return '&divide;'
      } else {
        return 'UNKNOWN'
      }
    },
    buildQuestion() {
      return `${this.qa.question.n1} ${this.operation()} ${this.qa.question.n2} =`
    },
  },
  computed: {
    divClass() {
      return {
        'correct-answer': this.answeredAndCorrect(),
      }
    },
  },
}
</script>

<template>
  <div class="single-question-answer" :class="divClass">
    <p v-html="buildQuestion()"></p>
    <input type="text" placeholder="?" class="answer-input" v-model="qa.answer.stringValue" />

    <img v-if="answeredAndCorrect()" src="../assets/check-circle.svg" />
    <img v-else src="../assets/circle.svg" />
  </div>
</template>
