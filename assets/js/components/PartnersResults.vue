<template>
<div class="results-viz">
<div class="svg-container">
  <svg viewBox="0 0 90 18"  preserveAspectRatio="none">
    <g class="chart">
    </g>
  </svg>
</div>
  <img src="/assets/imgs/cubes.svg">
</div>
</template>


<style lang="less">
.results-viz {

    img {
        display: block;
        position: relative;
        margin-top: -51px;
        width: 100.5%;
        // opacity: .5;
    }

    .svg-container {
        width: 100%;
        text-align: center;
        svg {
            width: 70%;
        }
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
        total : 50,
        percentage : 20,
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
