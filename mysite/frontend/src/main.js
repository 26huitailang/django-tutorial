import Vue from "vue";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import "vue-awesome/icons";
import Icon from "vue-awesome/components/Icon";
import axios from "axios";
import App from "./App";
import "./plugins/element.js";
import router from "./router";
import VueLazyload from "vue-lazyload";

Vue.use(VueLazyload, {
  preLoad: 1.3,
  error: require("@/assets/img/error-80.png"),
  loading: require("@/assets/img/loading.gif"),
  attempt: 1
});

Vue.config.productionTip = false;

Vue.use(ElementUI);

Vue.component("icon", Icon);
Vue.prototype.axios = axios;

/* eslint-disable no-new */
new Vue({
  el: "#app",
  router,
  template: "<App/>",
  components: { App }
});
