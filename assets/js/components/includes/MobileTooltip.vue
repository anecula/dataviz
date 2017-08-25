<template>
<div>
    <slot></slot>
</div>

</template>


<style lang="less">

</style>


<script>
import Vue from 'vue';

import ComponentMixin from '../mixins/Component.js'


export default Vue.extend({
  mixins: [ComponentMixin],

  props: {
  },

  computed: {

  },

  methods: {

  },
})
</script>
