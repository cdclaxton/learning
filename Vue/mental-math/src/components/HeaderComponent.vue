<script lang="ts">
export default {
  props: {
    percentageComplete: Number,
  },
}
</script>

<template>
  <div class="header">
    <p class="title">Mental Math</p>
    <p class="percentage-complete">{{ percentageComplete }} &#x0025;</p>
  </div>
</template>
