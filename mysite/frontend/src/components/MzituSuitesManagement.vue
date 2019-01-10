<template>
  <MzituSuiteTable></MzituSuiteTable>
</template>

<script>
import MzituSuiteTable from './MzituSuiteTable.vue'
import { get } from '../http'
export default {
  name: "MzituSuitesManagement",
  components: { MzituSuiteTable },
  data() {
    return {
    };
  },
};
</script>
