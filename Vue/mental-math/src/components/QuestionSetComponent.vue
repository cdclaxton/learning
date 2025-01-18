<script lang="ts">
import QuestionComponent from './QuestionComponent.vue'
import { QuestionSet } from '../modules/question'

export default {
  components: {
    QuestionComponent,
  },
  props: {
    questionSet: QuestionSet,
  },
}
</script>

<template>
  <template v-for="q in questionSet.questionAnswers">
    <QuestionComponent :qa="q" />
  </template>
</template>
