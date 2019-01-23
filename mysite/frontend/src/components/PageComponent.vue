<template>
  <el-pagination
    v-if="clientWidth > 768"
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    :page-sizes="[10, 20, 50]"
    :current-page="currentPage"
    :page-size="pageSize"
    :pager-count="pagerCount"
    layout="sizes, total, prev, pager, next, jumper"
    :total="pageTotal"
  ></el-pagination>
  <el-pagination
    v-else
    @size-change="handleSizeChange"
    @current-change="handleCurrentChange"
    :page-sizes="pageSizes"
    :current-page="currentPage"
    :page-size="pageSize"
    :pager-count="pagerCount"
    layout="total, prev, pager, next"
    :total="pageTotal"
  ></el-pagination>
</template>

<script>
import constant from "./TheConstant.vue";

export default {
  name: "PageComponent",
  props: {
    pageSizes: Array, // 每页多少个
    currentPage: Number, // 当前页
    pageSize: Number, // 默认每页多少个
    pagerCount: Number,
    pageTotal: Number
  },
  data() {
    return {
      clientWidth: constant.clientWidth
    }
  },
  methods: {
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage;
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize;
    },
  }
};
</script>

<style scoped>
</style>
