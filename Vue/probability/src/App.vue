<script lang="js">
import Header from './components/Header.vue'
import Results from './components/Results.vue'
import Scenarios from './components/Scenarios.vue'
import { ProbabilityElement } from './modules/probability'

let result = [
  new ProbabilityElement(0, 0.1),
  new ProbabilityElement(1, 0.8),
  new ProbabilityElement(2, 0.1),
]

export default {
  components: {
    Header,
    Scenarios,
    Results,
  },
  data() {
    return {
      result: result,
    }
  },
}
</script>

<template>
  <!-- Header bar -->
  <Header />

  <!-- Container for the scenarios and the results-->
  <div class="container">
    <!-- Scenarios -->
    <Scenarios />

    <!-- Results -->
    <Results :valueToProbabilities="result" />
  </div>
</template>
