<script lang="ts">
import { defineComponent } from 'vue'
import { QuestionAnswer } from '../modules/question'

export default defineComponent({
  props: {
    qa: {
      type: QuestionAnswer,
      required: true,
    },
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
})
</script>

<template>
  <div class="single-question-answer" :class="divClass">
    <p v-html="buildQuestion()"></p>

    <input
      type="number"
      :value="qa.answer.stringValue"
      class="answer-input"
      @input="(event) => (qa.answer.stringValue = event.target.value)"
    />

    <img v-if="answeredAndCorrect()" src="../assets/check-circle.svg" />
    <img v-else src="../assets/circle.svg" />
  </div>
</template>
