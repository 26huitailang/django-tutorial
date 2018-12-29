import Vue from 'vue'
import VueRouter from 'vue-router'
import MzituSuites from '../components/MzituSuites.vue'
import MzituSuiteDetail from '../components/MzituSuiteDetail.vue'
import MzituTag from '../components/MzituTag.vue'
import MzituTagSuites from '../components/MzituTagSuites.vue'
import Error404 from '../components/Error404.vue';
Vue.use(VueRouter)

const routes = [
  // todo: home page
  { 'path': '/', redirect: '/mzitu/suites' },
  { 'path': '/mzitu/suites', 'name': 'mzitu-suite-list', component: MzituSuites },
  { 'path': '/mzitu/suites/:id', 'name': 'mzitu-suite-detail', component: MzituSuiteDetail },
  { 'path': '/mzitu/tags', 'name': 'mzitu-tags-list', component: MzituTag },
  { 'path': '/mzitu/tags/:id/suites', 'name': 'mzitu-tags-detail', component: MzituTagSuites, props: true },
  { 'path': '/404', 'name': '404', component: Error404 },
  { 'path': '*', redirect: '/404' },
]

const router = new VueRouter({
  routes
})
export default router;