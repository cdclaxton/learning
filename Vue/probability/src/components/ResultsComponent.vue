<script lang="js">
import BarGraphComponent from './BarGraphComponent.vue'
import { DiscreteDistribution } from '../modules/scenarios.js'

export default {
  props: {
    distribution: DiscreteDistribution,
  },
  components: {
    BarGraphComponent,
  },
}
</script>

<template>
  <div class="results">
    <p class="results-header">Result</p>
    <div class="results-table">
      <!-- Header row -->
      <div class="results-table-header">Value</div>
      <div class="results-table-header">Probability</div>

      <!-- Data row -->
      <template v-for="e in distribution.elements">
        <div>{{ e.valueInput.value() }}</div>
        <div>{{ e.probabilityInput.probability() }}</div>
      </template>
    </div>

    <!-- Graph -->
    <BarGraphComponent :data="distribution" />
  </div>
</template>
