<script lang="js">
import ScenarioComponent from './ScenarioComponent.vue'

export default {
  props: {
    scenarios: Array,
  },
  components: {
    ScenarioComponent,
  },
  emits: ['evtAddScenario', 'evtDeleteScenario'],
  methods: {
    addScenario() {
      this.$emit('evtAddScenario')
    },
    deleteScenario(idx) {
      this.$emit('evtDeleteScenario', idx)
    },
  },
}
</script>

<template>
  <div class="scenarios">
    <template v-for="(s, idx) in scenarios">
      <ScenarioComponent :scenario="s" :scenarioIdx="idx" @evtDeleteScenario="deleteScenario" />
    </template>

    <!-- Button to add a new scenario -->
    <button class="add-scenario-button" @click="addScenario">+</button>
  </div>
</template>
