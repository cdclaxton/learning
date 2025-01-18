<script lang="ts">
import { defineComponent } from 'vue'
import QuestionComponent from './QuestionComponent.vue'
import { QuestionSet } from '../modules/question'

export default defineComponent({
  components: {
    QuestionComponent,
  },
  props: {
    questionSet: {
      type: QuestionSet,
      required: true,
    },
  },
})
</script>

<template>
  <template v-for="q in questionSet.questionAnswers">
    <QuestionComponent :qa="q" />
  </template>
</template>
