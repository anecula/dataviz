<template>
  <div class="projects">
    <div class="programme-item-header" @click="getProjects"> {{ name }} </div>
    <div v-if="posts.length != 0" class="programme-sublist-wrapper">
      <small class="programme-sublist-header">{{ sector }} ({{ posts.count}} {{ pluralize('project', posts.count) }})</small>
      <ul class="programme-sublist">
        <li class="programme-sublist-item"
            v-for="value of posts.results">
             <a v-if="value.url" :href=value.url target="_blank">{{ value.name }}</a>
             <span v-if="!value.url">{{ value.name }}</span>
         </li>
      </ul>
      <div v-if="posts.next" class="show-more small muted align-center">
         <button @click="showMore" type="button" class="btn-link">show {{ show_more_count }} more results</button>
       </div>
    </div>
  </div>
</template>

<style lang="less">
.dataviz .viz .projects {
  .programme-sublist-wrapper {
    .show-more {
        &:before,&:after {
          content:' — ';
          color: #3D90F3;
      }
    }
  }
  .programme-sublist-item {
    list-style-type: inherit;
    span {
      color: #444;
    }
  }
  .programme-item-header {
    position: relative;
    color: #444;
    padding-left: 2rem;
    display: block;
    cursor: pointer;
    &:hover {
      text-decoration: underline;
    }
  }

  .programme-item-header.active {
    color: #005494;
    border-top: 1px solid #ddd;
    padding-top: 1rem;
  }
  .active.programme-item-header{
      &:before {
          transform: rotate(90deg);
          top: 13px;
      }
  }

  .programme-sublist-header {
    margin-left: 2rem;
  }

  .programme-item-header:before {
    content: "\25BA";
    margin-right: .5rem;
    transition: all 300ms;
    left: 4px;
    font-size: 1.1rem;
    position: absolute;
  }

  .programme-sublist {
      margin-left: 3.5rem;
  }

  .spinning:after {
    content: '';
    position: absolute;
    top: -11px;
    height: 37px;
    width: 37px;
    background: url(/assets/imgs/spinner.svg);
    right: -20px;
    transform: scale(0.6);
  }
}
</style>

<script>
import Vue from 'vue';
import axios from 'axios';

import WithFiltersMixin from '../mixins/WithFilters';
import ComponentMixin from '../mixins/Component'

export default Vue.extend({
  mixins: [
    WithFiltersMixin,
    ComponentMixin,
  ],

  props: {
    detailsDatasource: String,
    id: String,
    country: String,
    sector: String,
    name: String,
    extra: String,
  },

  data() {
    return {
      posts: [],
      errors: [],
    }
  },

  computed: {
    show_more_count() {
      const count = this.posts.count - this.posts.results.length
      return count < 10 ? count : 10
    },
  },

  methods: {
    getProjects() {
      let target = this.$el.querySelector('.programme-item-header')
      target.classList.add('spinning')
      target.classList.toggle('active')

      if (this.posts.length == 0) {
        let url=`${this.detailsDatasource}?beneficiary=${this.country}&programme=${this.id}`
        if (this.filters.donor) {
          url = url + '&donor=' + this.filters.donor
        }
        if (this.filters.fm) {
          url = url + '&fm=' + this.filters.fm
        }
        if (this.filters.sector) {
          url = url + '&sector=' + this.filters.sector
        }
        if (this.filters.area) {
          url = url + '&area=' + this.filters.area
        }
        if (this.filters.region) {
          url = url + '&nuts=' + this.filters.region
        }
        if (this.extra) {
          // e.g. isDpp=true
          url = url + '&' + this.extra;
        }
        axios
          .get(url)
          .then(response => {
            this.posts = response.data;

            if(target.classList.contains('spinning'))
              target.classList.remove('spinning')
          })
          .catch(e => {
            this.errors.push(e)
          });
      }
      else {
        if(target.classList.contains('spinning'))
          target.classList.remove('spinning');
        this.posts = [];
      }
    },

    showMore() {
      let href = this.posts.next;
      if(href){
        axios.get(""+href+"")
          .then(response => {
            this.posts.next = response.data.next
            this.posts.count = response.data.count
            this.posts.previous = response.data.previous

            this.posts.results.push.apply(this.posts.results, response.data.results);
          })
          .catch(e => {
            this.errors.push(e)
        });
      }
    },
    handleFilterRegion() {
      this.posts = [];
      const target = this.$el.querySelector('.programme-item-header')
      target.classList.remove('active')
    },
  },

  watch: {
    'filters': {
      deep: true,
      handler() {
        this.posts = [];
        const target = this.$el.querySelector('.programme-item-header')
        target.classList.remove('active')
      },
    },
  },

});

</script>
