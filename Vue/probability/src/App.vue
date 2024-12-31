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
      console.log("Received 'load example' event")
      this.scenarios = exampleScenarios()
      console.log(this.scenarios.toString())
    },
    receiveClear() {
      console.log("Received 'clear' event")
      this.scenarios.clear()
      console.log(this.scenarios.toString())
    },
    receiveAddScenario() {
      console.log("Received 'add scenario' event")
      this.scenarios.addScenario()
      console.log(this.scenarios.toString())
    },
    receiveCalculate() {
      console.log("Received 'calculate' event")
      console.log(this.scenarios.toString())
      this.scenarios.calculate(100)
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
    <ScenariosComponent :scenarios="scenarios.scenarios" @evtAddScenario="receiveAddScenario" />

    <!-- Results -->
    <ResultsComponent :elements="scenarios.result.elements" />
  </div>
</template>
