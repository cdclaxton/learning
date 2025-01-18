<script lang="ts">
import HeaderComponent from './components/HeaderComponent.vue'
import QuestionSetComponent from './components/QuestionSetComponent.vue'
import { generateListQuestions, QuestionSet } from './modules/question'

export default {
  components: {
    HeaderComponent,
    QuestionSetComponent,
  },
  data() {
    // Generate a random set of questions
    const questions = generateListQuestions(10, 1, 100)
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
