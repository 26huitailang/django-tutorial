<template>
  <el-table
    :data="tableMzituTags"
    style="width: 100%">
    <el-table-column
      label="喜欢"
      width="180">
      <template slot-scope="scope">
        <el-switch
          v-model=scope.row.is_like
          @change="handleLikeToggle(scope.row.id, !scope.row.is_like, scope.$index)"
          active-color="#13ce66"
          inactive-color="#ff4949">
        </el-switch>
      </template>
    </el-table-column>
    <el-table-column
      label="标签"
      width="180">
      <template slot-scope="scope">
        <el-popover trigger="hover" placement="top">
          <p>{{ scope.row.url }}</p>
          <div slot="reference" class="name-wrapper">
            <el-tag size="medium">{{ scope.row.name }}</el-tag>
          </div>
        </el-popover>
      </template>
    </el-table-column>
    <el-table-column label="操作">
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="handleLikeToggle(scope.$index, scope.row)">编辑</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script>
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
      this.axios
        .get("http://127.0.0.1:8000/api/v1/mzitu/tags/")
        .then(response => (
          this.tableMzituTags = response.data
        ))
    },
    methods: {
      handleLikeToggle(id, is_like, index) {
        console.log(id, is_like);
        this.axios
          .post('http://127.0.0.1:8000/api/v1/mzitu/tags/' + id + '/like_toggle/')
          .then(response => (
            this.tableMzituTags[index].is_like = response.data.is_like
          ));
        console.log(id, this.tableMzituTags[index].is_like)
      },
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
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>
