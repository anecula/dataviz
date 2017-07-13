<template>
  <headroom>
    <div>
     <div class="header-logo">
     {{data}}
          <a href="/">
            <img src="/assets/imgs/eeaglogo.svg" alt="EEA Grants logo">
          </a>
        </div>
        <nav class="header-menu">
          <ul>
            <!-- <li><a href="{% url 'frontend:grants' %}"{% if current_view == 'frontend:grants' %} class="active"{% endif %}>Grants</a></li> -->
            <!-- <li><a href="{% url 'frontend:partners' %}"{% if current_view == 'frontend:partners' %} class="active"{% endif %}>Partners</a></li> -->
            <!-- <li><a href="{% url 'frontend:projects' %}"{% if current_view == 'frontend:projects' %} class="active"{% endif %}>Projects</a></li> -->
          </ul>
        </nav>
        <form action="/search/" class="header-search">
          <input type="search" placeholder="Search" name="q">
          <button type="submit" title="Search" name="page" value="1">
            <span class="icon icon-search"></span>
          </button>
        </form>

        <button type="button" class="header-toggle header-search-toggle" title="Search" onclick="Header.toggle('search')">
          <span class="icon icon-search"></span>
        </button>
        <button type="button" class="header-toggle header-menu-toggle" title="Menu" onclick="Header.toggle('menu')">
          <span class="icon icon-menu"></span>
        </button>
    </div>
  </headroom>
</template>

<script>
import Vue from 'vue'
import headroom from 'vue-headroom'

export default Vue.extend({
  components: {
    headroom
  },

  computed: {
    data() {
        console.log('lol')
        return 'test'
    }
  }


})
</script>
