<template>
  <MzituSuiteCard :suites="suites"></MzituSuiteCard>
</template>

<script>
import MzituSuiteCard from "./MzituSuiteCard.vue";
import { get } from "../http";
export default {
  name: "MzituSuites",
  components: { MzituSuiteCard },
  data() {
    return {
      suites: []
    };
  },
  mounted() {
    let tag_id = this.$route.query.tag_id;
    if (tag_id) {
      this.getSuitesByTagId(tag_id);
    } else {
      this.getSuites();
    }
  },
  watch: {
    $route(to) {
      if (to.query.tag_id) {
        this.getSuitesByTagId(to.query.tag_id);
      } else {
        this.getSuites();
      }
    }
  },
  methods: {
    getSuitesByTagId(id) {
      get(`mzitu/tags/${id}/suites/`).then(
        response => (this.suites = response.data)
      );
    },
    getSuites() {
      get("mzitu/suites/").then(response => (this.suites = response.data));
    }
  }
};
</script>
