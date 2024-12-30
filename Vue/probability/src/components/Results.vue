<script lang="js">
export default {
  props: {
    valueToProbabilities: Array,
  },
}
</script>

<template>
  <div class="results">
    <p class="results-header">Results</p>
    <div class="results-table">
      <!-- Header row -->
      <div class="results-table-header">Value</div>
      <div class="results-table-header">Probability</div>

      <!-- Data row -->
      <template v-for="item in valueToProbabilities">
        <div>{{ item.value }}</div>
        <div>{{ item.probability }}</div>
      </template>
    </div>
  </div>
</template>
