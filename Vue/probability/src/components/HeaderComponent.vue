<script lang="js">
export default {
  emits: ['evtLoadExample', 'evtClear', 'evtCalculate'],
  methods: {
    example() {
      this.$emit('evtLoadExample')
    },
    clear() {
      this.$emit('evtClear')
    },
    calculate() {
      this.$emit('evtCalculate')
    },
  },
}
</script>

<template>
  <div class="header">
    <div class="header-left">
      <div class="icon-div"></div>
      <p class="title-text">Scenario Consequences</p>
    </div>
    <div class="header-right">
      <button class="header-right-button" @click="example()">Example</button>
      <button class="header-right-button" @click="clear()">Clear</button>
      <button class="header-right-button" @click="calculate()">Calculate</button>
    </div>
  </div>
</template>
