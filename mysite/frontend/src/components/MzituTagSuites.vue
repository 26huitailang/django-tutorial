<template>
  <mzitu-suite-card :msg="msg" :suites="suites"></mzitu-suite-card>
</template>

<script>
import MzituSuiteCard from './MzituSuiteCard.vue'
import { get } from '../http'
export default {
  name: "MzituTagSuites",
  props: { id: String },
  components: { MzituSuiteCard },
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
