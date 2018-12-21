<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <ul>
      <li v-for="(item, index) in items" v-bind:key="item.id">{{ index }}. {{ item.url }} {{item.max_page }}</li>
      <!-- todo: not support absolute path -->
      <img src="/Users/chensijian/Desktop/super-luck.jpg" />
    </ul>
  </div>
</template>

<script>
  export default {
    name: "HelloWorld",
    props: {
      msg: String
    },
    data() {
      return {
        items: []
      };
    },
    mounted() {
      this.axios
        .get("http://127.0.0.1:8000/api/v1/mzitu/suite/")
        .then(response => (
          this.items = response.data
        ))
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
