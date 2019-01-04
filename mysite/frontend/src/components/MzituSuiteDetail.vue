<template>
  <div class="hello">
    <h1>{{ suite_title }}</h1>
    <el-table
      header-row-class-name="center"
      :data="currentPageImages"
      row-style="margin: 0 auto;"
      style="width: 800px;">
      <el-table-column
        align="center"
        prop="image"
        :label="title"
        >
        <template slot-scope="scope">
          <img :key="scope.row.id"
            v-lazy="getImgUrl(scope.row.image)"
            @click="handleImgClick"
            class="image" alt="" />
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :page-sizes="[1, 3, 5]"
      :current-page="currentPage"
      :page-size="pageSize"
      :pager-count="pagerCount"
      layout="sizes, total, prev, pager, next, jumper"
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
      pageSize: 1,
      allImages: [],
      pagerCount: 6,
      title: "Unknown"
    };
  },
  methods: {
    getImgUrl: function (media_url) {
      return apiBase() + media_url
    },
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize
    },
    // todo: 点击图片翻页的操作，之后用漂亮的弹窗替换
    handleImgClick() {
      if (this.currentPage === this.allImages.length) {
        alert("已经是最后一页")
      } else {
        this.currentPage += 1
      }
    }
  },
  computed: {
    currentPageImages: function () {
      return this.allImages.slice(this.pageSize * (this.currentPage - 1), this.pageSize * this.currentPage)
    },
  },
  mounted() {
    this.axios
      .get(MZITU().SuitesList + this.$route.params.id)
      .then(response => (
        this.allImages = response.data.images,
        this.title = response.data.name
      ))
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .el-table {
    height: 100%;
    margin: 0 auto;
  }
  .el-table__body {
    width: 100%;
    margin: 0 auto;
  }
  .el-table__header {
    width: 100%;
    margin: 0 auto;
  }
  a {
    color: #42b983;
  }
  img[lazy="loaded"] {
  }
  .image {
    margin: 10px auto;
    width: 500px;
    height: 100%;
    display: block;
  }
</style>
