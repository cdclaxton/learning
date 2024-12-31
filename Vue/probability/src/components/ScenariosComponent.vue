<script lang="js">
import ScenarioComponent from './ScenarioComponent.vue'

export default {
  props: {
    scenarios: Array,
  },
  components: {
    ScenarioComponent,
  },
  emits: ['evtAddScenario'],
  methods: {
    addScenario() {
      this.$emit('evtAddScenario')
    },
  },
}
</script>

<template>
  <div class="scenarios">
    <template v-for="s in scenarios">
      <ScenarioComponent :scenario="s" />
    </template>

    <!-- Button to add a new scenario -->
    <button class="add-scenario-button" @click="addScenario">+</button>
  </div>
</template>
