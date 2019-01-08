<template>
  <div id="app">
    <img src="./assets/logo.png" width="50px">
    <!-- <MzituSuite msg="Welcome to Your Mzitu App"/> -->
    <el-tabs type="border-card" v-model="activeName" @tab-click="handleTabClick">
      <el-tab-pane label="Suites" name="suites"></el-tab-pane>
      <el-tab-pane label="Tags" name="tags"></el-tab-pane>
      <!-- 路由对应的组件渲染的地方 -->
      <router-view></router-view>
    </el-tabs>
  </div>
</template>

<script>

export default {
  name: 'app',
  data() {
    return {
      activeName: this.getCurrentActiveName(),
    }
  },
  methods: {
    handleTabClick() {
      switch (this.activeName) {
        case "suites":
          this.$router.push('/mzitu/suites');
          break;
        case "tags":
          this.$router.push('/mzitu/tags');
          break;
        default:
          this.$router.push('/mzitu/suites')
          break;
      }
    },
    getCurrentActiveName() {  // 解决Tabs刷新初始化的问题
      const currentRoute = this.$router.currentRoute.path
      if (currentRoute.startsWith('/mzitu/suites')) {
        return 'suites'
      } else if (currentRoute.startsWith('/mzitu/tags')) {
        return 'tags'
      }
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 1em;
}
</style>
