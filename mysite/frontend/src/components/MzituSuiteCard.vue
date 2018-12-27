<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <el-row>
      <el-col :span="8" v-for="(item, index) in suites" :key="item.id" :offset="index > 0 ? 2 : 0">
        <el-card :body-style="{ padding: '0px', height: '180px' }" shadow="hover">
          <!-- todo: development usage -->
          <img :src="'http://127.0.0.1:8000' + item.images[0].image" class="image">
          <div style="padding: 14px;">
            <router-link
              :to="{ name: 'mzitu-suite-detail', params: { id: item.id }}"
            >{{ index }}. {{ item.name }} {{item.max_page }}</router-link>
            <div class="bottom clearfix">
              <!-- todo: loop for tags -->
              <el-tag size="mini">标签3</el-tag>
              <el-button type="text" class="button">标签2</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "MzituSuiteCard",
  props: {
    msg: String,
    suites: Array
  }
};
</script>

<style scoped>
.time {
  padding: 0;
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}
</style>
