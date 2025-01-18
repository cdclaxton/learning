<script lang="ts">
import HeaderComponent from './components/HeaderComponent.vue'
import QuestionSetComponent from './components/QuestionSetComponent.vue'
import { generateTailoredQuestions, QuestionSet } from './modules/question'

export default {
  components: {
    HeaderComponent,
    QuestionSetComponent,
  },
  data() {
    // Generate a random set of questions
    const questions = generateTailoredQuestions(10)
    const questionSet = new QuestionSet(questions)

    return {
      questionSet: questionSet,
    }
  },
}
</script>

<template>
  <!-- Header component -->
  <HeaderComponent :percentageComplete="questionSet.percentageComplete()" />

  <!-- Question set (i.e. list of questions) -->
  <QuestionSetComponent :questionSet="questionSet" />
</template>
