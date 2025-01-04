<script lang="js">
import * as d3 from 'd3'
import { DiscreteDistribution } from '../modules/scenarios.js'

export default {
  props: {
    data: {
      type: DiscreteDistribution,
      required: true,
    },
  },
  data() {
    return {
      width: 0, // width of the bar graph
      height: 0, // height of the bar graph
      svg: null, // SVG element
      x: null, // x-axis scaling function
      xAxis: null, // x-axis
      y: null, // y-axis scaling function
      yAxis: null, // y-axis
    }
  },
  mounted() {
    this.createChart()
  },
  watch: {
    data: 'updateChart',
  },
  methods: {
    createChart() {
      console.log('Creating chart')
      console.log(this.data)

      // Calculate the dimensions of the bar graph
      const margin = { top: 10, right: 30, bottom: 70, left: 60 }
      this.width = 500 - margin.left - margin.right
      this.height = 300 - margin.top - margin.bottom

      // Append an SVG object
      this.svg = d3
        .select(this.$refs.chart)
        .append('svg')
        .attr('width', this.width + margin.left + margin.right)
        .attr('height', this.height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.right})`)

      // Initialise the x-axis
      this.x = d3.scaleBand().range([0, this.width]).padding(0.2)
      this.xAxis = this.svg.append('g').attr('transform', `translate(0, ${this.height})`)

      // Initialise the y-axis
      this.y = d3.scaleLinear().range([this.height, 0])
      this.yAxis = this.svg.append('g').attr('class', 'myYaxis')

      // X-axis label
      this.svg
        .append('text')
        .attr('class', 'xLabel')
        .attr('text-anchor', 'end')
        .attr('x', this.width)
        .attr('y', this.height + margin.top + 20)
        .text('Value')

      // Y-axis label
      this.svg
        .append('text')
        .attr('class', 'yLabel')
        .attr('text-anchor', 'end')
        .attr('transform', 'rotate(-90)')
        .attr('y', -margin.left + 20)
        .attr('x', -margin.top)
        .text('Probability')

      this.updateChart()
    },
    updateChart() {
      console.log('Updating chart')
      console.log(this.data)

      // Update the x-axis
      this.x.domain(this.data.elements.map((e) => e.valueInput.value()))
      this.xAxis.call(d3.axisBottom(this.x))

      // Update the y-axis
      this.y.domain([0, d3.max(this.data.elements, (e) => e.probabilityInput.probability())])
      this.yAxis.transition().duration(1000).call(d3.axisLeft(this.y))

      let u = this.svg.selectAll('rect').data(this.data.elements)

      u.join('rect')
        .transition()
        .duration(1000)
        .attr('x', (e) => this.x(e.valueInput.value()))
        .attr('y', (e) => this.y(e.probabilityInput.probability()))
        .attr('width', this.x.bandwidth())
        .attr('height', (e) => this.height - this.y(e.probabilityInput.probability()))
        .attr('fill', '#69b3a2')
    },
  },
}
</script>

<template>
  <!-- Div in which to place the bar graph -->
  <div ref="chart"></div>
</template>
