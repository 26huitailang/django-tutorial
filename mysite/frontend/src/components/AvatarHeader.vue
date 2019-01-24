<template>
  <el-dropdown>
    <span class="el-dropdown-link">
      <Avatar :username="username" />
    </span>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item>Info</el-dropdown-item>
      <el-dropdown-item divided>
        <span @click="handleLogout">Logout</span>
      </el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>
import Avatar from "vue-avatar";
export default {
  name: "AvatarHeader",
  components: { Avatar },
  props: {
    username: String
  },
  methods: {
    handleLogout() {
      this.$message({ message: "logout", type: "success" });
      sessionStorage.clear();
      this.$emit("logout");
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
.el-dropdown {
  margin-bottom: 15px;
}
</style>
