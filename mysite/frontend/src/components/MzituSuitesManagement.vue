<template>
  <MzituSuiteTable :tableData="suites"></MzituSuiteTable>
</template>

<script>
import MzituSuiteTable from './MzituSuiteTable.vue'
import { get } from '../http'
export default {
  name: "MzituSuitesManagement",
  components: { MzituSuiteTable },
  data() {
    return {
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
