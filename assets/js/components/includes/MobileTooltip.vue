<template>
<div>
<ul>
    <li>
        {{data.id}}
    </li>
    <li>
        {{data.sectors.size()}} {{singularize('sectors', data.sectors.size())}}
    </li>
    <li>
        {{data.areas.size()}} {{singularize('programme areas' , data.areas.size())}}
    </li>
    <li>
        {{data.programmes.size()}} {{singularize('programmes', data.programmes.size())}}
    </li>
</ul>
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
    data: Object,
  },

  computed: {

  },

  methods: {

  },
})
</script>
