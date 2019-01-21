<template>
  <div>
    <el-table
      :data="currentPageData()"
      style="width: 550px;margin-left: auto;margin-right: auto;"
      :row-style="rowStyle"
      :header-row-style="headerRowStyle"
      :cell-style="cellStyle"
      :header-cell-style="cellStyle"
      :default-sort="{prop: 'is_like', order: 'descending'}"
    >
      <el-table-column sortable fixed prop="is_like" label="喜欢" width="100%">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.is_like"
            @change="handleLikeToggle(scope.row.id, scope.row.is_like, scope.$index)"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column sortable prop="tag" label="标签">
        <template slot-scope="scope">
          <el-tag size="medium">
            <a :href="scope.row.url" target="_blank" :title="scope.row.name">
              <div class="tag-name">{{ scope.row.name }}</div>
            </a>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="数量" sortable prop="suites_count" width="100%">
        <template slot-scope="scope">
          <a @click="handleClickTagCount(scope.row.id)">{{ scope.row.suites_count }}</a>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot="header" slot-scope="scope">
          <el-input v-model="search" size="mini" placeholder="输入标签名搜索"/>
        </template>
        <template slot-scope="scope">
          <!-- <el-button
            type="primary"
            icon="el-icon-edit"
            circle
            size="mini"
          @click="handleLikeToggle(scope.$index, scope.row)"></el-button>-->
          <el-button
            type="danger"
            icon="el-icon-delete"
            circle
            size="mini"
            @click="handleDeleteTag(scope.row.id)"
          ></el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :page-sizes="[10, 20, 50]"
      :current-page="currentPage"
      :page-size="pageSize"
      :pager-count="pagerCount"
      layout="sizes, total, prev, pager, next, jumper"
      :total="filterData.length"
    ></el-pagination>
  </div>
</template>
<script>
import { get, post, _delete } from "../http";
import { MZITU } from "../http/api.js";
export default {
  name: "MzituTag",
  props: {},
  data() {
    return {
      tableMzituTags: [],
      currentPage: 1,
      pageSize: 10,
      pagerCount: 5,
      search: ""
    };
  },
  mounted() {
    this.getList();
  },
  computed: {
    filterData() {
      let result = this.tableMzituTags.filter(
        data =>
          !this.search ||
          data.name.toLowerCase().includes(this.search.toLowerCase())
      );
      return result
    },
  },
  methods: {
    currentPageData() {
      return this.filterData.slice(
        this.pageSize * (this.currentPage - 1),
        this.pageSize * this.currentPage
      );
    },
    getList() {
      get("mzitu/tags/").then(
        response => (this.tableMzituTags = response.data)
      );
    },
    rowStyle({ row, rowIndex }) {
      return "height: 45px;font-size: 12px;";
    },
    headerRowStyle() {
      return "height: 55px";
    },
    cellStyle() {
      return "padding: 0; text-align: center;";
    },
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage;
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize;
    },
    handleLikeToggle(id, is_like, index) {
      // 这个scope传入的index和tableMzituTags 不是同一个排序
      post("mzitu/tags/" + id + "/like_toggle/")
        .then(response =>
          // 这种写法vue不是响应式的，返回新的对象
          // this.tableMzituTags[index].is_like = response.data.is_like
          this.tableMzituTags.forEach(function(item) {
            if (item.id === id) {
              item.is_like = response.data.is_like;
            }
          })
        )
        .catch(error =>
          this.tableMzituTags.forEach(function(item) {
            if (item.id === id) {
              item.is_like = is_like;
            }
          })
        );
    },
    handleClickTagCount(id) {
      this.$router.push(`/mzitu/suites?tag_id=${id}`);
    },
    handleDeleteTag(id) {
      this.$confirm("此操作将永久删除该文件, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          _delete(MZITU(id).TagDelete)
            .then(() => {
              this.$message({
                type: "success",
                message: "删除成功!"
              });
              this.getList();
            })
            .catch(error => {
              this.$message({
                type: "error",
                message: error.data
              });
            });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    }
  },
  watch: {
    $route(to) {
      this.$router.push({ name: to.name, params: to.params });
      get("mzitu/tags/").then(
        response => (this.tableMzituTags = response.data)
      );
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
