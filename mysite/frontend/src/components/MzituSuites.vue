<template>
  <!-- <MzituSuiteTemplate :msg="msg" :suites="suites"></MzituSuiteTemplate> -->
  <MzituSuiteCard :msg="msg" :suites="suites"></MzituSuiteCard>
</template>

<script>
import MzituSuiteTemplate from './MzituSuiteTemplate.vue'
import MzituSuiteCard from './MzituSuiteCard.vue'
import { get } from '../http'
export default {
  name: "MzituSuites",
  components: { MzituSuiteCard },
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
