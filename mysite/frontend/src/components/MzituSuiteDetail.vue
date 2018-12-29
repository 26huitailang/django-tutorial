<template>
  <div class="hello">
    <h1>{{ suite_title }}</h1>
    <!-- <ul>
      <li v-for="(item, index) in images" v-bind:key="item.id">{{ index + 1 }}.
        <div class="cover">
          <img :src="'http://192.168.2.101:8000' + item.image" class="image" />
        </div>
      </li> -->
    <!-- </ul> -->
      <!-- todo: not support absolute path -->
      <el-row :gutter="10">
        <el-col :span="24"
          v-for="(item, index) in currentPageImages" :key="item.id"
        >
          <!-- {{ index + 1 }}<img :src="getImgUrl(item.image)" class="image" /> -->
          {{ index + 1 }}<img v-lazy="getImgUrl(item.image)" class="image" alt="" />
        </el-col>
      </el-row>
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-size="pageSize"
        :pager-count="6"
        layout="prev, pager, next"
        :total="allImages.length">
      </el-pagination>
  </div>
</template>

<script>
import { apiBase, MZITU } from "../http/api.js";
export default {
  name: "MzituSuiteDetail",
  props: {
    suite_title: String
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      allImages: [],
    };
  },
  methods: {
    getImgUrl: function (media_url) {
      return apiBase() + media_url
    },
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage
    }
  },
  computed: {
    currentPageImages: function () {
      return this.allImages.slice(this.pageSize * (this.currentPage - 1), this.pageSize * this.currentPage)
    }
  },
  mounted() {
    this.axios
      .get(MZITU().SuitesList + this.$route.params.id)
      .then(response => (
        this.allImages = response.data.images
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
  img[lazy="loaded"] {
  }
  .image {
    margin: 10px 0 0;
    width: 500px;
    height: 100%;
    display: block;
  }
</style>
