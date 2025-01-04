<script lang="js">
import HeaderComponent from './components/HeaderComponent.vue'
import ResultsComponent from './components/ResultsComponent.vue'
import ScenariosComponent from './components/ScenariosComponent.vue'
import { Scenarios, exampleScenarios } from './modules/scenarios'

export default {
  components: {
    HeaderComponent,
    ScenariosComponent,
    ResultsComponent,
  },
  data() {
    return {
      scenarios: new Scenarios(),
    }
  },
  methods: {
    receiveLoadExample() {
      this.scenarios = exampleScenarios()
    },
    receiveClear() {
      this.scenarios.clear()
    },
    receiveAddScenario() {
      this.scenarios.addScenario()
    },
    receiveCalculate() {
      this.scenarios.calculate(100)
    },
    receiveDeleteScenario(idx) {
      this.scenarios.deleteScenario(idx)
    },
  },
}
</script>

<template>
  <!-- Header bar -->
  <HeaderComponent
    @evtLoadExample="receiveLoadExample"
    @evtClear="receiveClear"
    @evtCalculate="receiveCalculate"
  />

  <!-- Container for the scenarios and the results-->
  <div class="container">
    <!-- Scenarios -->
    <ScenariosComponent
      :scenarios="scenarios.scenarios"
      @evtAddScenario="receiveAddScenario"
      @evtDeleteScenario="receiveDeleteScenario"
    />

    <!-- Results -->
    <ResultsComponent :distribution="scenarios.result" />
  </div>
</template>
