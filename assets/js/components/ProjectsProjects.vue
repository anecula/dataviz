<template>
    <ul class="programmes" v-if="hasData">
      <li v-for="beneficiary in data.beneficiaries">
        <div class="content-item programmes_content">
          <div class="body">
            <div @click="toggleContent($event)" class="title-wrapper">
                <div class="flag">
                    <img :src="`/assets/imgs/${get_flag_name(beneficiary.id)}.png`"/>
                </div>
                <h3 class="title">{{ get_country_name(beneficiary.id) }}</h3>
                <small>({{ beneficiary.programmes.length }} programmes)</small>
            </div>
            <ul class="programme-list" :class="[{ active : filters.beneficiary }]">
               <li v-for="programme in beneficiary.programmes"
                   class="programme-item">
                 <div class="programme-item-header" :country="beneficiary.id" :id="programme.programme_code" @click="getProjects($event)"> {{ programme.programme_name }} </div>
                   <div v-if="posts"  class="programme-sublist-wrapper">
                   <small key="results.name"  class="programme-sublist-header">{{ programme.sector }}</small>
                      <ul class="programme-sublist">
                       <!--     <li v-if="posts" class="programme-sublist-item"
                              v-for="results of programme.projects.results"
                           >
                              {{ results.name }}
                           </li> -->
                      </ul>
                      <div class="show-more small muted align-center">
                              &ndash;
                              <button @click="showMore($event)" :next="programme.next" type="button" class="btn-link">show 10 more results</button>
                              &ndash;
                      </div>
                  </div>
               </li>
            </ul>
          </div>
        </div>
      </li>
    </ul>
</template>

<style lang="less">
.programmes{
  li {
    list-style-type: none;
    color: inherit;
  }

  small {
    color: #898989;
  }

  .programme-list {
    margin-left: .5rem;
    padding-left: 0;
    color: #444;
  }

  .programme-sublist {
    padding-left: 0;
    margin-left: 2rem;
    li {
      margin: 1rem 0;
    }

    li:before {
      content: "●";
      margin-right: .5rem;
      color: #3D90F3;
    }

  }

  .title-wrapper:hover {
    text-decoration: underline;
  }

  .flag {
    width: 30px;
    height: 20px;
    img {
        width: 100%;
    }
  }

  .ind-count {
    display: inline;
    font-size: 2rem;
    color: black;
  }

  .title {
    color: #444;
  }

  .programme-item-header:before {
    display: inline-block;
    content: "►";
    margin-right: .5rem;
    transition: all 300ms;
  }

  .programme-item {
    margin: 1rem 0;
    font-size: 1.3rem;
  }

  .programme-item-header {
    display: inline;
    cursor: pointer;
  }

  .active .programme-item-header{
    color: #005494;
    &:before {
        transform: rotate(90deg);
    }
  }

  .programme-list {
    display: none;
  }

  .programme-list.active {
    display: block;
  }


  .title-wrapper > * {
    display: inline-block;
    margin-right: .5rem;
  }

  .title-wrapper {
    display: flex;
    cursor: pointer;
    align-items: center;
    margin: 1rem 0;
  }

  .country_thumbnail {
    display: inline-block;
    width: 24px;
    margin-right: .5rem;
  }

  div.small,
  .programme-sublist-header {
    display: none;
  }
  .programme-item.active small,
  .programme-item.active div.small {
    display: block;
  }

}
</style>

<script>

import Vue from 'vue';
import * as d3 from 'd3';
import axios from 'axios';

import BaseMixin from './mixins/Base';
import WithCountriesMixin, {COUNTRIES, get_flag_name} from './mixins/WithCountries';

export default Vue.extend({
  mixins: [
    BaseMixin, WithCountriesMixin,
  ],


 data() {
    return {
      posts: [],
      errors: []
      }
    },

  computed: {
    projectcount() {
      // this could be useful to the parent?

      // NOTE: WARNING: TODO: this sum is in fact wrong, because a programme
      // can belong to multiple PAs. the sum per-beneficiary needs to be
      // provided by the backend.

      return data.projectcount;
    },



    data() {
      const dataset = this.filter(this.dataset);
      const beneficiaries = {};
      let totalcount = 0;
      for (const d of dataset) {
        const programmes = d.programmes;

        if (!programmes || !Object.keys(programmes).length) continue;

        let beneficiary = beneficiaries[d.beneficiary];
        if (beneficiary === undefined)
          beneficiary = beneficiaries[d.beneficiary] = {
            _projectcount: 0,
          };

        for (const p in programmes) {
          // TODO: clean the project count logic
          const projectcount = 0;
          //const projectcount = +programmes[p];
          //if (projectcount == 0) continue;
          let programme = beneficiary[p];
          if (programme === undefined)
            programme = beneficiary[p] = {
              sector: d.sector,
              programme_code: p,
              programme_name: programmes[p].name,
              programme_url: programmes[p].url,
              projectcount: 0,
              projects : [],
              next : null
            };


          programme.projectcount += projectcount;
          beneficiary._projectcount += projectcount;
          totalcount += projectcount;
        }
      }

      const out = {
        beneficiaries: [],
        projectcount: totalcount,
      };

      for (const b in beneficiaries) {
        const programmes = beneficiaries[b],
              beneficiary = {
                id: b,
                programmes: [],
              };
        let benef = beneficiary.id

        out.beneficiaries.push(beneficiary);
        for (const p in programmes) {
          const value = programmes[p];
          if (p === '_projectcount') {
            beneficiary.projectcount = value;
            continue;
          }
          beneficiary.programmes.push(value);
        }
      }

      //Sort by country
      out.beneficiaries.sort((a,b) => d3.ascending(this.get_country_name(a.id),this.get_country_name(b.id)));
      return out;
    },
  },

  methods: {

    getProjects(e) {
      let programme_code = e.target.getAttribute('id');
      let country_code = e.target.getAttribute('country');
      let target = e.target.parentNode.querySelector('.programme-sublist');
      let test = e.target.parentNode.querySelectorAll('.programme-sublist li')
      let active_item = e.target.parentNode;
      if(active_item.classList.contains('active')){
        active_item.classList.remove('active')
      }
      else{
        active_item.classList.add('active')
      }

     if(test.length == 0){
      axios.get(`/api/projects/?beneficiary=${country_code}&programme=${programme_code}`)
      .then(response => {
        this.posts = response.data
        for (let d of this.data.beneficiaries){
            for (let b of d.programmes) {
              if(b.programme_code == programme_code )
                  {
                    b.next = this.posts.next
                    for (let r of this.posts.results){
                    var node = document.createElement("LI");
                    var textnode = document.createTextNode(r.name);
                    node.appendChild(textnode);
                    target.appendChild(node);
                    }
                  }
             }
        }

      })
      .catch(e => {
        this.errors.push(e)
      });

      }

      else {
          test.forEach(function(item, i){
            target.removeChild(item)
          });


      }

    },

    showMore(e) {
      let next = e.target.getAttribute('next');
      let target = e.target.parentNode.parentNode.parentNode.querySelector('.programme-sublist');
      let nextNode = target.parentNode.querySelector('.show-more')
      if(this.posts.next){
      axios.get(""+next+"").then(response => {
        this.posts = response.data
        for (let r of this.posts.results){
            var node = document.createElement("LI");
            var textnode = document.createTextNode(r.name);
            node.appendChild(textnode);
            target.appendChild(node);
          }
          e.target.setAttribute('next',this.posts.next)
          if(this.posts.next==null){
            target.parentNode.removeChild(nextNode);
          }
      })
        .catch(e => {
          this.errors.push(e)
        });
      }


    },


    toggleContent(e) {
      //remove comment if you want to toggle between elements

      // let all_programe_items = this.$el.querySelectorAll('.programme-item');
      // for (let item of all_programe_items){
      //     if(item.classList.contains('active'))
      //         item.classList.remove('active')
      // }

      //TODO : get rid of the parenNode logic
      let target;
      if (e.target.parentNode.classList.contains('flag'))
        target = e.target.parentNode.parentNode.parentNode.querySelector('.programme-list');
      else
         target = e.target.parentNode.parentNode.querySelector('.programme-list');
      if(target.classList.contains('active')){
        target.classList.remove('active')
      }
      else {
        target.classList.add('active')
      }
    },
  },
});

</script>
