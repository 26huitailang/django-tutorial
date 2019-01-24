<template>
  <div>
    <el-row type="flex" align="middle" justify="end">
      <el-col :span="6">
        <el-input clearable v-model="search" size="mini" placeholder="输入名称搜索" style="margin-bottom: 10px;"/>
      </el-col>
    </el-row>
    <el-row :gutter="10">
      <el-col
        :xs="24" :sm="8" v-for="item in searchSuites" :key="item.id" :offset="0">
        <el-card
          :body-style="{ padding: '10px', height: cardHeight }"
          shadow="hover">
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
              <p>{{ item.name }} | {{ item.max_page }}张</p>
            </router-link>
            <div class="bottom clearfix">
              <el-tag size="mini" v-for="tag in item.tags" :key="tag.id">
                <router-link :to="{ name: 'mzitu-suites-card', query: { tag_id: tag.id }}">
                  {{ tag.name }}
                </router-link>
              </el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { apiBase } from "../http/api.js";

export default {
  name: "MzituSuiteCard",
  props: {
    suites: Array
  },
  data() {
    return {
      cardHeight: "470px",
      search: ""
    };
  },
  computed: {
    searchSuites() {
      // 也能搜索tags
      return this.suites.filter(
        data =>
          !this.search ||
          data.name.toLowerCase().includes(this.search.toLowerCase()) ||
          // 这里写个function返回true false，判断是否tag也符合搜索条件
          this.tagsWithTextBoolean(data.tags, this.search)
      );
    }
  },
  methods: {
    coverImage(media_url) {
      return apiBase() + media_url;
    },
    tagsWithTextBoolean(array, text) {
      for (let i = 0; i < array.length; i++) {
        if (array[i].name.toLowerCase().includes(text.toLowerCase())) {
          return true;
        }
      }
      return false;
    }
  }
};
</script>

<style scoped>
a {
  color: steelblue;
  text-decoraction: none;
}

p {
  font-size: 12px;
  overflow: hidden;
  width: 100%;
  white-space: nowrap;
  text-overflow: ellipsis;
  text-align: center;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

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
