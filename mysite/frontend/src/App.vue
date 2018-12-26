<template>
  <div id="app">
    <img src="./assets/logo.png">
    <div>
      <p>
        If Element is successfully added to this project, you'll see an
        <code v-text="'<el-button>'"></code>
        below
      </p>
    </div>
    <ul>
      <li><router-link to="/mzitu/suites">Suite</router-link></li>
      <li><router-link to="/mzitu/tags">Tags</router-link></li>
    </ul>
    <!-- <MzituSuite msg="Welcome to Your Mzitu App"/> -->
    <router-view></router-view>
  </div>
</template>

<script>
// import MzituSuite from './components/MzituSuite.vue'
// import MzituSuiteDetail from './components/MzituSuiteDetail.vue'
// import MzituTag from './components/MzituTag.vue'

export default {
  name: 'app',
  components: {
    // MzituSuite,
    // MzituSuiteDetail,
    // MzituTag,
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
  margin-top: 60px;
}
</style>
