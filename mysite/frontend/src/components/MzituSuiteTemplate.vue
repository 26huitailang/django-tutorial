<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <ul>
      <li v-for="(item, index) in suites" v-bind:key="item.id">
        <router-link :to="{ name: 'mzitu-suite-detail', params: { id: item.id }}">{{ index }}. {{ item.url }} {{item.max_page }}</router-link>
      </li>
      <!-- todo: not support absolute path -->
    </ul>
  </div>
</template>

<script>
export default {
  name: "MzituSuiteTemplate",
  props: {
    msg: String,
    suites: Array,
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h3 {
    margin: 40px 0 0;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    /* display: inline-block; */
    margin: 0 10px;
    text-align: left;
  }

  a {
    color: #42b983;
  }
</style>
