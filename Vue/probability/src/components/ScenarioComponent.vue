<script lang="js">
import { Scenario } from '../modules/scenarios.js'

export default {
  props: {
    scenario: Scenario,
    scenarioIdx: Number,
  },
  methods: {
    normalise() {
      this.scenario.normalise()
    },
    addRow() {
      this.scenario.addElement('', '')
    },
    deleteScenario() {
      this.$emit('evtDeleteScenario', this.scenarioIdx)
    },
  },
  computed: {
    scenarioErrorClass() {
      return {
        'scenario-error': !this.scenario.isValid(),
      }
    },
  },
}
</script>

<template>
  <div class="scenario" :class="scenarioErrorClass">
    <div class="scenario-detail">
      <!-- Button to delete the scenario -->
      <button class="delete-scenario" @click="deleteScenario">&times;</button>

      <!-- Text box for the scenario name -->
      <input
        class="scenario-name"
        type="text"
        placeholder="Scenario name"
        v-model="scenario.name"
      />

      <!-- Table for the probability distribution -->
      <div class="scenario-prob-table">
        <!-- Header row -->
        <div>Value</div>
        <div>Probability</div>
        <div></div>

        <!-- Data rows -->
        <template v-for="(e, idx) in scenario.distribution.elements">
          <!-- Value -->
          <input type="text" v-model="e.valueInput.stringValue" />

          <!-- Probability -->
          <input type="text" v-model="e.probabilityInput.stringValue" />

          <!-- Delete row button -->
          <button class="delete-probability-row" @click="scenario.distribution.deleteElement(idx)">
            &times;
          </button>
        </template>
      </div>

      <!-- Buttons to add and normalise probabilities -->
      <div class="probability-buttons">
        <button class="add-probability-row" @click="addRow">+</button>
        <button class="normalise-probabilities" @click="normalise">Normalise</button>
      </div>
    </div>

    <!-- Probability of the scenario occurring -->
    <div class="scenario-prob-div">
      <p>p =</p>
      <input
        class="scenario-prob"
        type="text"
        placeholder="1.0"
        v-model="scenario.probabilityInput.stringValue"
      />
    </div>
  </div>
</template>
