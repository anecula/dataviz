<template>
  <transition-group
      tag="ul"
      class="results"
      name="viz"
  >
    <li
        v-for="(item, outcome) in data"
        :key="`outcome:${outcome}`"
    >
      <div class="content-item results_content">
        <div class="body">
          <h4 class="title">{{ outcome }}</h4>
          <small v-show="!filters.sector">{{ item.sector }}</small>
          <transition-group
              tag="ul"
              class="indicators"
              name="viz"
          >
            <li
                v-for="(value, indicator) in item.indicators"
                class="indicator clearfix"
                :style="{borderColor: sectorcolour(item.sector)}"
                :key="`indicator:${indicator}`"
            >
              <div class="indicator-achievement"> {{ value }}</div>
              <div class="indicator-name"> {{ indicator }} </div>
            </li>
          </transition-group>
        </div>
      </div>
    </li>
  </transition-group>
</template>

<style lang="less">
.results {
  li {
    list-style-type: none;
  }

  ul {
    padding-left: 0;
  }

  small {
    color: #898989;
  }

  .indicator {
    border-left: 3px solid red;
    margin-bottom: .5rem;
    padding-left: .5rem;
  }

  .indicator-achievement {
    display: inline;
    font-size: 2rem;
    color: black;
  }

  .indicator-name {
    display: inline;
    font-size: 1.2rem;

  }

}
</style>

<script>

import Vue from 'vue';
import * as d3 from 'd3';
import BaseMixin from './mixins/Base';
import WithSectorsMixin from './mixins/WithSectors';
import {FILTERS} from '../globals.js'

export default Vue.extend({
  mixins: [
    BaseMixin, WithSectorsMixin,
  ],

  computed: {
    data() {
      if (!this.hasData) return {};

      const dataset = this.filter(this.dataset);
      const results = {};

      for (const d of dataset) {
        for (const o in d.results) {
          const values = d.results[o];

          if (!values) continue;

          let outcome = results[o];
          if (outcome === undefined)
            outcome = results[o] = {
              sector: d.sector,
              indicators: {},
            };

          for (let i in values) {
            const value = +values[i];

            if (value === 0) continue;

            i = i.replace(/^Number of /, '');

            let sum = outcome.indicators[i] || 0;
            outcome.indicators[i] = sum + value;
          }
        }
      }

      // TODO: sorting order?

      return results;
    },
  },
});

</script>
