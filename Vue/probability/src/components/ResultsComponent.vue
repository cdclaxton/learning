<script lang="js">
export default {
  props: {
    elements: Array,
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
      <template v-for="e in elements">
        <div>{{ e.valueInput.value() }}</div>
        <div>{{ e.probabilityInput.probability() }}</div>
      </template>
    </div>
  </div>
</template>
