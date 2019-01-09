<template>
  <div>
    <el-table
      :data="currentPageData"
      style="width: 100%"
      :row-style="rowStyle"
      :header-row-style="headerRowStyle"
      :cell-style="cellStyle"
      :header-cell-style="cellStyle"
      :default-sort="{prop: 'created_time', order: 'descending'}"
    >
      <el-table-column sortable prop="created_time" label="日期" width="150px"></el-table-column>
      <el-table-column prop="name" label="名称" width="100%"></el-table-column>
      <el-table-column sortable prop="tag" label="标签" width="150px">
        <template slot-scope="scope">
          <el-dropdown size="mini" split-button type="primary">
            {{ scope.row.tags.length }}
            <el-dropdown-menu slot="dropdown">
              <span v-for="tag in scope.row.tags" :key="tag.id">
                <router-link :to="{ name: 'mzitu-tags-detail', params: { id: tag.id }}">
                  <el-dropdown-item>
                    <el-tag size="mini">{{ tag.name }}</el-tag>
                  </el-dropdown-item>
                </router-link>
              </span>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
      <el-table-column label="图片" sortable width="100%">
        <template slot-scope="scope">
          <el-popover placement="right-end" title="预览" width="400" trigger="hover">
            <div class="block">
              <el-carousel type="card" height="300px" style="text-align: center">
                <el-carousel-item v-for="item in scope.row.images.slice(0, 5)" :key="item.id">
                  <img :src="getPreviewImage(item.image)" style="height: 300px;margin: 0 auto;">
                </el-carousel-item>
              </el-carousel>
            </div>
            <el-button slot="reference">
              <a @click="handleClickCount(scope.row.id)">{{ scope.row.images.length }}</a>
            </el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100%">
        <template slot-scope="scope">
          <el-button
            type="primary"
            icon="el-icon-edit"
            circle
            size="mini"
            @click="handleLikeToggle(scope.$index, scope.row)"
          ></el-button>
          <el-button
            type="danger"
            icon="el-icon-delete"
            circle
            size="mini"
            @click="handleLikeToggle(scope.$index, scope.row)"
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
      :total="tableData.length"
    ></el-pagination>
  </div>
</template>
<script>
import { get, post } from "../http";
import { apiBase, MZITU } from "../http/api.js";
export default {
  name: "MzituSuiteTable",
  props: {
    tableData: Array
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      pagerCount: 5
    };
  },
  mounted() {},
  computed: {
    currentPageData: function() {
      return this.tableData.slice(
        this.pageSize * (this.currentPage - 1),
        this.pageSize * this.currentPage
      );
    }
  },
  methods: {
    rowStyle({ row, rowIndex }) {
      return "height: 45px;font-size: 12px;";
    },
    headerRowStyle() {
      return "height: 55px";
    },
    cellStyle() {
      return "padding: 0; text-align: center;";
    },
    getPreviewImage(media_url) {
      return apiBase() + media_url;
    },
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage;
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize;
    },
    handleLikeToggle(id, is_like, index) {
      // 这个scope传入的index和tableData 不是同一个排序
      post("mzitu/tags/" + id + "/like_toggle/")
        .then(response =>
          // 这种写法vue不是响应式的，返回新的对象
          // this.tableData[index].is_like = response.data.is_like
          this.tableData.forEach(function(item) {
            if (item.id === id) {
              item.is_like = response.data.is_like;
            }
          })
        )
        .catch(error =>
          this.tableData.forEach(function(item) {
            if (item.id === id) {
              item.is_like = is_like;
            }
          })
        );
    },
    handleClickCount(id) {
      this.$router.push({ name: "mzitu-suites-detail", params: { id: id } });
    }
  },
  watch: {
    $route(to, from) {
      this.$router.push({ name: to.name, params: to.params });
      get("mzitu/tags/").then(response => (this.tableData = response.data));
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
.el-carousel__item img {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  width: 100%;
  height: 360px;
  left: 50%;
  display: block;
  object-fit: cover;
  position: relative;
  -webkit-transform: translateX(-50%);
	-ms-transform: translateX(-50%);
	-moz-transform: translateX(-50%);
}
.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
