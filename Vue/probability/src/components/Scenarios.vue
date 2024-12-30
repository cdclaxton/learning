<script lang="js">
import Scenario from './Scenario.vue'

export default {
  components: {
    Scenario,
  },
}
</script>

<template>
  <div class="scenarios">
    <Scenario />
    <Scenario />

    <!-- Button to add a new scenario -->
    <button class="add-scenario-button">+</button>
  </div>
</template>
