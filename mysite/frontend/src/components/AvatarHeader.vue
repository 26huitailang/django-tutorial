<template>
  <el-dropdown>
    <span class="el-dropdown-link">
      <avatar
        :username=username
        :customStyle=customStyle
        ></avatar>
    </span>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item>Info</el-dropdown-item>
      <el-dropdown-item divided>Logout</el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>
import Avatar from "vue-avatar";
export default {
  name: "AvatarHeader",
  components: { Avatar },
  data() {
    return {
      username: "4 0 4",
    }
  },
  methods: {
    customStyle() {
      return "margin-bottom: 15px";
    }
  },
  mounted() {
      let username = sessionStorage.getItem('user_name');
      if (username) {
        return this.username = username
      }
  }
}
</script>

<style scoped>
.el-dropdown {
  margin-bottom: 1em,
}
</style>
