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

    img {
        display: block;
        position: relative;
        margin-top: -46px;
        width: 100.5%;
    }
}


</style>


<script>
import Vue from 'vue';
import * as d3 from 'd3';

import BaseMixin from './mixins/Base';
import ChartMixin from './mixins/Chart';


export default Vue.extend({
  mixins: [
    BaseMixin, ChartMixin
  ],

  data(){
    return {
        total : 100,
        percentage : 35,
    }
  },

  computed: {
    data() {
      const out = [this.total, this.percentage]
      return out;
    },

  },

  methods: {
    renderChart() {
      const $this = this,
            chart = this.chart;
        console.log(this.data)

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
        .attr("height", y)
        .transition()
        .attr("width", x)
        .attr('fill', function(d) {
            if(d==$this.data[0])
                return "#aaa"
            else
                return 'rgb(10, 160, 70)'
        })
    },


  },
});

</script>
