<template>
  <el-table
    :data="tableMzituTags"
    style="width: 100%"
    :default-sort="{prop: 'is_like', order: 'descending'}"
    >
    <el-table-column
      sortable
      fixed
      prop="is_like"
      label="喜欢"
      width="80px">
      <template slot-scope="scope">
        <el-switch
          v-model=scope.row.is_like
          @change="handleLikeToggle(scope.row.id, scope.row.is_like, scope.$index)"
          active-color="#13ce66"
          inactive-color="#ff4949">
        </el-switch>
      </template>
    </el-table-column>
    <el-table-column
      sortable
      prop="tag"
      label="标签"
      width="150px">
      <template slot-scope="scope">
        <el-tag size="medium">
          <a :href=scope.row.url target="_blank" :title="scope.row.name">
            <div class="tag-name">{{ scope.row.name }}</div>
          </a>
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column
      label="数量"
      sortable
      prop="suites_count"
      width="100%">
      <template slot-scope="scope">
        <a @click="handleClickTagCount(scope.row.id)">{{ scope.row.suites_count }}</a>
      </template>
    </el-table-column>
    <el-table-column label="操作">
      <template slot-scope="scope">
        <el-button
          type="primary"
          icon="el-icon-edit"
          circle
          size="mini"
          @click="handleLikeToggle(scope.$index, scope.row)"></el-button>
        <el-button
          type="danger"
          icon="el-icon-delete"
          circle
          size="mini"
          @click="handleLikeToggle(scope.$index, scope.row)"></el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script>
import { get, post } from '../http'
export default {
  name: "MzituTag",
  props: {
    msg: String
  },
  data() {
    return {
      tableMzituTags: [],
    };
  },
  mounted() {
    get("mzitu/tags/")
      .then(response => (
        this.tableMzituTags = response.data
      ))
  },
  methods: {
    handleLikeToggle(id, is_like, index) {  // 这个scope传入的index和tableMzituTags 不是同一个排序
      post('mzitu/tags/' + id + '/like_toggle/')
        .then(response => (
          // 这种写法vue不是响应式的，返回新的对象
          // this.tableMzituTags[index].is_like = response.data.is_like
          this.tableMzituTags.forEach(function (item) {
            if (item.id === id) {
              item.is_like = response.data.is_like
            }
          })
        ))
        .catch(error => (
          console.log(error, error.response),
          this.tableMzituTags.forEach(function (item) {
            if (item.id === id) {
              item.is_like = is_like
            }
          })
        ))
    },
    handleClickTagCount(id) {
      this.$router.push(`/mzitu/tags/${id}/suites`)
    }
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
  .tag-name {
    overflow: hidden;
    width: 100px;
    white-space: nowrap;
    text-overflow: ellipsis;
    text-align: center;
  }
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
  .el-button {
    margin: 10px 0;
    display: inline-block;
  }
</style>
