<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <el-row>
      <el-col :span="elColSpan" v-for="(item, index) in suites" :key="item.id" :offset="elColOffset">
        <el-card :body-style="{ padding: '10px' }" shadow="hover">
          <!-- todo: development usage -->
          <div class="cover">
            <img :src="'http://192.168.2.101:8000' + item.images[0].image" class="image">
          </div>
          <div style="padding: 14px;">
            <router-link
              :to="{ name: 'mzitu-suite-detail', params: { id: item.id }}"
            >{{ index }}. {{ item.name }} {{item.max_page }}</router-link>
            <div class="bottom clearfix">
              <!-- todo: loop for tags -->
              <el-tag size="mini">标签1</el-tag>
              <el-tag size="mini">标签3</el-tag>
              <!-- <el-button type="text" class="button">标签2</el-button> -->
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
  },
  data () {
    return {
      elColSpan: 22,
      elColOffset: 0,
    }
  },
  beforeMount: function () {
    //可用于设置自适应屏幕，根据获得的可视宽度（兼容性）判断是否显示
    let w = document.documentElement.offsetWidth || document.body.offsetWidth;
    if (w < 1000) {
      this.elColSpan = 22
    } else {
      this.elColSpan = 8
    }
    if (this.elColSpan > 8) {
      this.elColOffset = 1
    } else {
      this.elColOffset = 0
    }
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

/* .cover {
  margin: 10px auto;
  width: 100%;
  height: 240px;
  overflow: hidden;
  position: relative;
} */
.image {
  width: 100%;
  height: 300px;
  left: 50%;
  display: block;
  object-fit: cover;
  position: relative;
  -webkit-transform: translateX(-50%);
	-ms-transform: translateX(-50%);
	-moz-transform: translateX(-50%);
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
