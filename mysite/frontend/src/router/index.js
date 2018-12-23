import Vue from 'vue'
import VueRouter from 'vue-router'
import MzituSuite from '../components/MzituSuite.vue'
import MzituSuiteDetail from '../components/MzituSuiteDetail.vue'
Vue.use(VueRouter)

const routes = [
  { 'path': '*', redirect: '/mzitu' },
  { 'path': '/mzitu', 'name': 'mzitu', component: MzituSuite },
  { 'path': '/mzitu/:id', 'name': 'mzitu-detail', component: MzituSuiteDetail },
]

const router = new VueRouter({
  routes
})
export default router;