<template>
  <div>
    <MzituSuitesCard :suites="suites" @handleSearchClick="handleSearchClick"/>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :page-sizes="pageSizes"
      :current-page="currentPage"
      :page-size="pageSize"
      :pager-count="pagerCount"
      :layout="layout"
      :total="total"
    ></el-pagination>
  </div>
</template>

<script>
import MzituSuitesCard from "./MzituSuitesCard.vue";
import { get } from "../http";
export default {
  name: "MzituSuites",
  components: { MzituSuitesCard },
  data() {
    return {
      suites: [],
      currentPage: 1,
      pageSizes: [9, 18, 36],
      pageSize: 9,
      pagerCount: 5,
      total: 0,
      layout: "sizes, total, prev, pager, next, jumper",
      search: ""
    };
  },
  mounted() {
    let tag_id = this.$route.query.tag_id;
    if (tag_id) {
      this.getSuitesByTagId(tag_id);
    } else {
      this.getSuites();
    }
  },
  watch: {
    $route(to) {
      if (to.query.tag_id) {
        this.getSuitesByTagId(to.query.tag_id);
      } else {
        this.getSuites();
      }
    }
  },
  methods: {
    getSuitesByTagId(id) {
      get(`mzitu/tags/${id}/suites/`).then(
        response => (this.suites = response.data)
      );
    },
    getSuites() {
      get(
        `mzitu/suites/?page=${this.currentPage}&page_size=${this.pageSize}&search=${this.search}`
      ).then(response => {
        this.suites = response.data.results;
        this.total = response.data.count;
      });
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize;
      this.getSuites();
    },
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage;
      this.getSuites();
    },
    handleSearchClick(search) {
      this.search = search;
      this.getSuites();
    },
  }
};
</script>
