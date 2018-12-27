<template>
  <MzituSuiteTemplate :msg="msg" :suites="suites"></MzituSuiteTemplate>
</template>

<script>
import MzituSuiteTemplate from './MzituSuiteTemplate.vue'
import { get } from '../http'
export default {
  name: "MzituSuites",
  components: { MzituSuiteTemplate },
  data() {
    return {
      msg: "Mzitu Suites",
      suites: [],
    };
  },
  mounted() {
    get("mzitu/suites/")
      .then(response => (
        this.suites = response.data
      ))
  }
};
</script>
