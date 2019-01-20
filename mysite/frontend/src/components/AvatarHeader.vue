<template>
  <el-dropdown>
    <span class="el-dropdown-link">
      <avatar
        :username=username
        ></avatar>
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
  data() {
    return {
      username: "N-/-A",
    }
  },
  methods: {
    handleLogout() {
      this.$message({ message: "logout", type: "success"})
      sessionStorage.clear()
      this.$router.push('/login')
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
  margin-bottom: 15px
}
</style>
