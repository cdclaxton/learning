<script lang="ts">
import HeaderComponent from './components/HeaderComponent.vue'
import QuestionSetComponent from './components/QuestionSetComponent.vue'
import { generateTailoredQuestions, Question, QuestionSet } from './modules/question'

export default {
  components: {
    HeaderComponent,
    QuestionSetComponent,
  },
  data() {
    return {
      questionSet: this.generateQuestions(),
    }
  },
  methods: {
    generateQuestions(): QuestionSet {
      // Generate a random set of questions
      const questions = generateTailoredQuestions(20)
      return new QuestionSet(questions)
    },
    receiveNewQuestionSet() {
      this.questionSet = this.generateQuestions()
    },
  },
}
</script>

<template>
  <!-- Header component -->
  <HeaderComponent
    :percentageComplete="questionSet.percentageComplete()"
    @evtNewQuestionSet="receiveNewQuestionSet"
  />

  <!-- Question set (i.e. list of questions) -->
  <QuestionSetComponent :questionSet="questionSet" />
</template>
