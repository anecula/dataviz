<template>
<div class="results-viz">
<div class="svg-container">
  <svg viewBox="0 0 100 14"  preserveAspectRatio="none">
    <g class="chart">
    </g>
  </svg>
  <img src="/assets/imgs/cubes.svg">
</div>
</div>
</template>


<style lang="less">
.results-viz {

    img {
      position: absolute;
      top: 15px;
      width: 202px;
      left: 59px;
      // opacity: 0.5;
    }

    .svg-container {
          width: 100%;
          text-align: center;
          max-width: 200px;
          margin: auto;
          height: 33px;
        svg {
          height: 100%;
          width: 100%;
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
        total : 100,
        percentage : 21,
    }
  },

  computed: {
    data() {
      const test = parseInt(this.percentage.toString().substring(1,2));
      let percentage = this.percentage;

      if(test != 0 && (6-test > 0)){
        percentage += 6-test
      }
      else if(test == 0 && this.percentage % 4 != 0 ) {
        percentage += 2.5
        console.log(percentage)
      }

      const out = [this.total, percentage]
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
