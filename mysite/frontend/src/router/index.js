import Vue from 'vue'
import VueRouter from 'vue-router'
import MzituSuite from '../components/MzituSuite.vue'
import MzituSuiteDetail from '../components/MzituSuiteDetail.vue'
import MzituTag from '../components/MzituTag.vue'
Vue.use(VueRouter)

const routes = [
  { 'path': '*', redirect: '/mzitu' },
  { 'path': '/mzitu', 'name': 'mzitu-suite-list', component: MzituSuite },
  { 'path': '/mzitu/:id', 'name': 'mzitu-suite-detail', component: MzituSuiteDetail },
  { 'path': '/mzitu/tags', 'name': 'mzitu-tags-list', component: MzituTag },
]

const router = new VueRouter({
  routes
})
export default router;