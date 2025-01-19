<script lang="ts">
export default {
  props: {
    percentageComplete: Number,
  },
  emits: ['evtNewQuestionSet'],
  methods: {
    newQuestionSet() {
      this.$emit('evtNewQuestionSet')
    },
  },
}
</script>

<template>
  <div class="header">
    <p class="title">Mental Math</p>
    <div class="header-right">
      <button class="button-new" @click="newQuestionSet()">
        <img src="../assets/refresh.svg" width="35px" />
      </button>
      <p class="percentage-complete">{{ percentageComplete }} &#x0025;</p>
    </div>
  </div>
</template>
