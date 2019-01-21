<template>
  <el-dropdown>
    <span class="el-dropdown-link">
      <avatar :username="username"></avatar>
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
  data() {
    return {
    };
  },
  methods: {
    handleLogout() {
      this.$message({ message: "logout", type: "success" });
      sessionStorage.clear();
      this.$emit('logout');
      this.$router.push("/login");
    },
    getUsername() {
      return sessionStorage.getItem("user_name") || "N-/-A  ";
    }
  },
  computed: {
    isUsernameChanged() {
      let nameInSession = this.getUsername();
      if (nameInSession === this.username) {
        return false
      } else {
        return true
      }
    },
  }
};
</script>

<style scoped>
.el-dropdown {
  margin-bottom: 15px;
}
</style>
