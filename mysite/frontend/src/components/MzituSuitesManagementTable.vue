<template>
  <div>
    <el-row type="flex" align="middle">
      <el-col :span="12">
        <el-button size="mini" @click="clearFilter">清除所有过滤器</el-button>
      </el-col>
      <el-col :span="12">
        <el-input clearable v-model="search" size="mini" placeholder="输入名称搜索"/>
      </el-col>
    </el-row>
    <el-table
      ref="suiteManageTable"
      :data="currentPageData()"
      style="width: 100%;"
      :row-style="rowStyle"
      :header-row-style="headerRowStyle"
      :cell-style="cellStyle"
      :header-cell-style="cellStyle"
      :default-sort="{prop: 'created_time', order: 'descending'}"
    >
      <el-table-column v-if="isShowCreatedTimeCol" sortable prop="created_time" label="日期" width="135px"></el-table-column>
      <el-table-column prop="name" label="名称" :show-overflow-tooltip="true" min-width="150px">
        <template slot-scope="scope">
          <a @click="handleClickCount(scope.row.id)">{{ scope.row.name }}</a>
        </template>
      </el-table-column>
      <el-table-column
        sortable
        prop="tag"
        label="标签"
        :filters="tagFilters"
        :filter-method="filterTag"
        width="120px"
      >
        <template slot-scope="scope">
          <!-- todo: 这个下拉写法用在移动端, 但是展开太多也不好看👎 -->
          <el-dropdown size="mini" split-button type="info">
            {{ scope.row.tags.length }}
            <el-dropdown-menu slot="dropdown">
              <span v-for="tag in scope.row.tags" :key="tag.id">
                <router-link :to="{ name: 'mzitu-suites-card', query: { tag_id: tag.id }}">
                  <el-dropdown-item>
                    <el-tag size="mini">{{ tag.name }}</el-tag>
                  </el-dropdown-item>
                </router-link>
              </span>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
      <el-table-column label="图片">
        <template slot-scope="scope">
          <el-popover placement="top" title="预览" :width="clientWidth > 768 ? 666 : 200" trigger="click">
            <div class="block">
              <el-carousel type="card" :height="clientWidth > 768 ? '300px' : '200px'" style="text-align: center">
                <el-carousel-item v-for="item in stepFilterImages(scope.row.images)" :key="item.id">
                  <img v-lazy="getPreviewImage(item.image)" style="height: 300px;margin: 0 auto;">
                </el-carousel-item>
              </el-carousel>
            </div>
            <el-button
              size="mini"
              slot="reference"
            >{{ scope.row.locals_count }}/{{ scope.row.max_page }}</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180px">
        <template slot="header" slot-scope="scope">
          <el-button type="text" @click="dialogVisible = true">添加</el-button>
        </template>
        <template slot-scope="scope">
          <el-popover
            trigger="click"
            placement="bottom-end"
            width="100"
            :ref="'popover-download-' + scope.$index"
          >
            <p>确认重新下载吗？</p>
            <div style="text-align: right; margin: 0">
              <el-button
                size="mini"
                type="text"
                @click="scope._self.$refs[`popover-download-${scope.$index}`].doClose()"
              >取消</el-button>
              <el-button type="primary" size="mini" @click="popoverSubmit(scope, 'download')">确定</el-button>
            </div>
            <el-button
              type="warning"
              size="mini"
              plain
              slot="reference"
              :disabled="scope.row.is_complete"
            >重新下载</el-button>
          </el-popover>
          <el-popover
            trigger="click"
            placement="bottom-end"
            width="100"
            :ref="'popover-delete-' + scope.$index"
          >
            <p>确认删除吗？</p>
            <div style="text-align: right; margin: 0">
              <el-button
                size="mini"
                type="text"
                @click="scope._self.$refs[`popover-delete-${scope.$index}`].doClose()"
              >取消</el-button>
              <el-button type="primary" size="mini" @click="popoverSubmit(scope, 'delete')">确定</el-button>
            </div>
            <el-button type="danger" size="mini" plain slot="reference">删除</el-button>
          </el-popover>
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
      :layout="layout"
      :total="filterData.length"
    ></el-pagination>
    <el-dialog title="下载" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
      <el-input placeholder="Suite or Theme URL" v-model="downloadSuiteUrl" clearable></el-input>
      <el-checkbox v-model="downloadIsTheme">isTheme</el-checkbox>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleClickAddSuite" :loading="loadingAddSuite">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import Vue from "vue";
import { get, post, _delete } from "../http";
import { apiBase, MZITU } from "../http/api.js";
import constant from "./TheConstant";

export default {
  name: "MzituSuitesManagementTable",
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      pagerCount: 5,
      popoverVisible: false,
      tableData: [],
      dialogVisible: false,
      downloadSuiteUrl: "",
      loadingAddSuite: false,
      tagFilters: [],
      clientWidth: constant.clientWidth,
      isShowCreatedTimeCol: constant.clientWidth > 992,  // md size
      search: "",
      websocket: null
    };
  },
  mounted() {
    this.getList();
    this.getTagFilters();
  },
  destroyed() {
    this.websocket.close();
  },
  computed: {
    filterData() {
      return this.tableData.filter(
        data =>
          !this.search ||
          data.name.toLowerCase().includes(this.search.toLowerCase())
      );
    },
    downloadIsTheme() {
      if (this.downloadSuiteUrl.indexOf("tag") > 0) {
        return true;
      }
      return false;
    },
    layout() {
      return constant.clientWidth > 768
        ? "sizes, total, prev, pager, next, jumper"
        : "total, prev, pager, next";
    }
  },
  methods: {
    currentPageData() {
      return this.filterData.slice(
        this.pageSize * (this.currentPage - 1),
        this.pageSize * this.currentPage
      );
    },
    // Style
    rowStyle() {
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
    popoverSubmit(scope, type) {
      if (type === "delete") {
        this.deleteSuite(scope);
      } else if (type === "download") {
        this.handleDownloadSuite(scope.row.url, scope.row.id); // todo 下载后轮训，试试dwebsocket
      }
      scope._self.$refs[`popover-${type}-${scope.$index}`].doClose();
    },
    deleteSuite(scope) {
      _delete(MZITU(scope.row.id).SuitesDetail)
        .then(response => {
          this.$message({ message: response.data, type: "success" });
          this.getList();
        })
        .catch(error => {
          this.$message({ message: error, type: "error" });
        });
    },
    handleDownloadSuite(url, suite_id) {
      post(MZITU().SuitesDownload + url)
        .then(response => {
          this.$message({ message: response.data, type: "success" });
          // todo: 下载的话就将ws推送回来的信息添加到tableData中，动态更新到页面上
          let username = sessionStorage.getItem('user_name');
          this.initWebsocket(`ws://localhost:8001/ws?username=${username}&suite_id=${suite_id}`)
        })
        .catch(error => {
          this.$message({ message: error, type: "error" });
        });
    },
    initWebsocket(ws_url) {
      let token = sessionStorage.getItem('token');
      this.websocket = new WebSocket(ws_url, [token]);  // 通过标准中可自定义的字段Sec-WebSocket-Protocol
      this.websocket.onmessage = this.websocketOnMessage;
      this.websocket.onclose = this.websocketOnClose;
    },
    websocketOnMessage(e) {
      let new_element = JSON.parse(e.data);

      for (let i = 0; i < this.tableData.length; i++) {
        if (this.tableData[i].id === new_element.id) {
          console.log('replace');
          Vue.set(this.tableData[i], 'locals_count', new_element.locals_count);
          if (new_element.max_page === new_element.locals_count) {
            Vue.set(this.tableData[i], 'is_complete', true);
          }
        }
      }
    },
    websocketOnClose(e) {
      console.log('断开', e);
    },
    getList() {
      get(MZITU().SuitesList).then(
        response => (this.tableData = response.data)
      );
    },
    getTagFilters() {
      // 获取过滤用的tags列表
      let tag_list = [];
      get(MZITU().Tags).then(response =>
        response.data.forEach(function(element) {
          let item = { text: element.name, value: element.name };
          tag_list.push(item);
        })
      );
      this.tagFilters = tag_list;
    },
    handleClickAddSuite() {
      this.loadingAddSuite = true;
      if (this.downloadIsTheme) {
        post(MZITU().ThemesDownload + this.downloadSuiteUrl)
          .then(response => {
            this.$message({ message: response.data, type: "success" });
          })
          .catch(error => {
            this.$message({ message: error, type: "error" });
          });
      } else {
        this.handleDownloadSuite(this.downloadSuiteUrl);
      }
      this.loadingAddSuite = false;
      this.dialogVisible = false;
    },
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage;
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize;
    },
    handleClickCount(id) {
      this.$router.push({ name: "mzitu-suites-detail", params: { id: id } });
    },
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then(() => {
          done();
        })
        .catch(() => {});
    },
    stepFilterImages(imagesList) {
      let step = Math.round(imagesList.length / 5); // 四舍五入
      step = step === 0 ? 1 : step; // 避免step 0 不能取余
      return imagesList.filter((element, index) => {
        return index % step === 0;
      });
    },
    clearFilter() {
      this.$refs.suiteManageTable.clearFilter();
    },
    filterTag(value, row) {
      let result = false;
      row.tags.forEach(function(element) {
        if (element.name === value) {
          result = true;
        }
      });
      return result;
    }
  },
  watch: {
    $route(to) {
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
