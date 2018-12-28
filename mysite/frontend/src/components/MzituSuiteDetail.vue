<template>
  <div class="hello">
    <h1>{{ suite_title }}</h1>
    <ul>
      <li v-for="(item, index) in images" v-bind:key="item.id">{{ index + 1 }}.
        <img :src="'http://192.168.2.101:8000' + item.image" />
      </li>
      <!-- todo: not support absolute path -->
    </ul>
  </div>
</template>

<script>
  export default {
    name: "MzituSuiteDetail",
    props: {
      suite_title: String
    },
    data() {
      return {
        images: []
      };
    },
    mounted() {
      this.axios
        .get("http://192.168.2.101:8000/api/v1/mzitu/suites/" + this.$route.params.id)
        .then(response => (
          this.images = response.data.images
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
