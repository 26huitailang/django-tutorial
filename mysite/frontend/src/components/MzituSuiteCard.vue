<template>
  <div class="hello">
    <el-row>
      <el-col
        :span="elColSpan" v-for="item in suites" :key="item.id" :offset="0">
        <el-card
          :body-style="{ padding: '10px', height: cardHeight }"
          shadow="hover">
          <!-- todo: development usage -->
          <div class="cover">
            <router-link
              :to="{ name: 'mzitu-suites-detail', params: { id: item.id }}"
              >
              <img v-lazy="coverImage(item.images[0].image)" class="image">
            </router-link>
          </div>
          <div style="padding: 5px 10px; height: 130px">
            <router-link
              :to="{ name: 'mzitu-suites-detail', params: { id: item.id }}"
              >
              <p style="font-size: 12px;">{{ item.name }} | {{ item.max_page }}张</p>
            </router-link>
            <div class="bottom clearfix">
              <!-- todo: loop for tags -->
              <el-tag size="mini" v-for="tag in item.tags" :key="tag.id">
                <router-link :to="{ name: 'mzitu-tags-detail', params: { id: tag.id }}">
                  {{ tag.name }}
                </router-link>
              </el-tag>
              <!-- <el-button type="text" class="button">标签2</el-button> -->
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { apiBase, MZITU } from "../http/api.js";
export default {
  name: "MzituSuiteCard",
  props: {
    suites: Array
  },
  data () {
    return {
      elColSpan: 24,
      elColOffset: 0,
      cardHeight: '470px',
    }
  },
  beforeMount: function () {
    //可用于设置自适应屏幕，根据获得的可视宽度（兼容性）判断是否显示
    let w = document.documentElement.offsetWidth || document.body.offsetWidth;
    if (w < 1000) {
      this.elColSpan = 24,
      this.cardHeight = '100%'
    } else {
      this.elColSpan = 8
    }
    if (this.elColSpan <= 8) {
      this.elColOffset = 1
    } else {
      this.elColOffset = 0
    }
  },
  methods: {
    coverImage (media_url) {
      return apiBase() + media_url
    }
  }
};
</script>

<style scoped>
a {
  color: steelblue;
  text-decoraction: none;
}
.el-card {
  margin: 1em 1em;
}
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
  height: 360px;
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
