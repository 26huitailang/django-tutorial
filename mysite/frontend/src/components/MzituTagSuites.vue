<template>
  <MzituSuiteTemplate :msg="msg" :suites="suites"></MzituSuiteTemplate>
</template>

<script>
import MzituSuiteTemplate from './MzituSuiteTemplate.vue'
import { get } from '../http'
export default {
  name: "MzituTagSuites",
  props: { id: String },
  components: { MzituSuiteTemplate },
  data() {
    return {
      msg: "Mzitu Tag-Suites",
      suites: [],
    };
  },
  mounted() {
    get(`mzitu/tags/${this.id}/suites/`)
      .then(response => (
        this.suites = response.data
      ))
  }
};
</script>
