import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import MzituSuites from '../components/MzituSuites.vue'
import MzituSuiteDetail from '../components/MzituSuiteDetail.vue'
import MzituTag from '../components/MzituTag.vue'
import MzituSuitesManagement from '../components/MzituSuitesManagement.vue'
import Error404 from '../components/Error404.vue';
Vue.use(VueRouter)

const routes = [
  // todo: home page
  { 'path': '/', redirect: '/mzitu/suites' },
  { 'path': '/login', name: 'login' , component: Login },
  { 'path': '/mzitu/suites', 'name': 'mzitu-suites-card', component: MzituSuites },
  { 'path': '/mzitu/suites/management', 'name': 'mzitu-suites-management', component: MzituSuitesManagement },
  { 'path': '/mzitu/suites/:id', 'name': 'mzitu-suites-detail', component: MzituSuiteDetail },
  { 'path': '/mzitu/tags', 'name': 'mzitu-tags-list', component: MzituTag },
  { 'path': '/404', 'name': '404', component: Error404 },
  { 'path': '*', redirect: '/404' },
]

const router = new VueRouter({
  routes
})
export default router;