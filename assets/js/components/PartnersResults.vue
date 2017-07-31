<template>
<div class="results-viz">
  <svg viewBox="0 0 100 14"  preserveAspectRatio="none">
    <g class="chart">
    </g>
  </svg>
  <img src="/assets/imgs/cubes.svg">
</div>
</template>


<style lang="less">
.results-viz {
    svg rect:first-of-type {
        color: #fff;
        fill: #aaa;
    }

    svg rect:nth-of-type(2) {
        color: #fff;
        stroke: transparent;
        fill: rgb(10, 160, 70);
    }

    img {
        display: block;
        position: relative;
        margin-top: -46px;
    }

}


</style>


<script>
import Vue from 'vue';
import * as d3 from 'd3';

import BaseMixin from './mixins/Base';
import ChartMixin from './mixins/Chart';
import WithSectors from './mixins/WithSectors';


export default Vue.extend({
  mixins: [
    BaseMixin, ChartMixin,WithSectors
  ],


  computed: {
    data() {
    const total = 100,
               percent = 50;

      const out = [total, percent]
      return out;
    },

  },

  methods: {
    renderChart() {
      const $this = this,
            chart = this.chart;

    const y = 14;
    const x = d3.scaleLinear()
    .domain([0, d3.max($this.data)])
    .range([0, 100]);

     chart
        .attr("class", "chart")
        .attr("width", 200)
        .attr("height", y);


    chart.selectAll("rect")
        .data($this.data)
        .enter().append("rect")
        .transition()
        .attr("width", x)
        .attr("height", y)
    },

  },
});

</script>
