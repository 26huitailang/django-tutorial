<template>
  <div id="app">
    <!-- <img src="./assets/logo.png" width="50px"> -->
    <avatar-header :username="username" @logout="getUsername"></avatar-header>
    <el-row type="flex" class="row-bg" justify="center">
      <el-col :xs="24" :sm="20" :md="12" :lg="18">
        <div class="container">
          <el-tabs type="border-card" v-model="activeName" @tab-click="handleTabClick">
            <el-tab-pane label="Suites" name="suites"></el-tab-pane>
            <el-tab-pane label="Tags" name="tags"></el-tab-pane>
            <el-tab-pane label="SuitesManage" name="suites-manage"></el-tab-pane>
            <!-- 路由对应的组件渲染的地方 -->
            <router-view @login="getUsername"></router-view>
          </el-tabs>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import AvatarHeader from "./components/AvatarHeader.vue";
export default {
  name: "app",
  components: { AvatarHeader },
  data() {
    return {
      activeName: "",
      username: ""
    };
  },
  methods: {
    handleTabClick() {
      switch (this.activeName) {
        case "suites":
          this.$router.push("/mzitu/suites");
          break;
        case "tags":
          this.$router.push("/mzitu/tags");
          break;
        case "suites-manage":
          this.$router.push({ name: "mzitu-suites-management" });
          break;
        default:
          this.$router.push("/mzitu/suites");
          break;
      }
    },
    getCurrentActiveName() {
      // 解决Tabs刷新初始化的问题
      const currentRouteName = this.$router.currentRoute.name;
      let result = "";
      if (currentRouteName.startsWith("mzitu-suites")) {
        result = "suites";
      } else if (currentRouteName.startsWith("mzitu-tags")) {
        result = "tags";
      }
      if (currentRouteName.indexOf("management") != -1) {
        result = "suites-manage";
      }
      this.activeName = result;
    },
    getUsername() {
      this.username = sessionStorage.getItem("user_name") || "N-/-A  ";
    }
  },
  mounted() {
    this.getCurrentActiveName();
    this.getUsername();
  },
  watch: {
    $route() {
      this.getCurrentActiveName();
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 1em;
}
.container {
  /* margin-left: 15%; */
  /* margin-right: 15%; */
}
</style>
