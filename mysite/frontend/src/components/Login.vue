<template>
  <div class="container">
    <el-form
      :model="loginForm"
      :rules="rules"
      ref="loginForm"
      label-width="100px"
      class="demo-loginForm"
    >
      <el-row type="flex" class="row-bg" justify="center">
        <el-col :xs="24" :sm="12">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="loginForm.username"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row type="flex" class="row-bg" justify="center">
        <el-col :xs="24" :sm="12">
          <el-form-item label="密码" prop="password">
            <el-input v-model="loginForm.password" type="password"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row type="flex" class="row-bg" justify="center">
        <el-form-item>
          <el-col :xs="24" :sm="24">
            <el-button type="primary" @click="submitForm('loginForm')">登陆</el-button>            <el-button @click="resetForm('loginForm')">重置</el-button>
          </el-col>
        </el-form-item>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import { post } from "../http";
import { AUTH } from "../http/api.js";
export default {
  name: "Login",
  data() {
    return {
      loginForm: {
        username: "",
        password: ""
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          {
            min: 3,
            max: 150,
            messge: "长度在 3 到 150 个字符",
            trigger: "blur"
          }
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { min: 3, messge: "长度至少 3 个字符", trigger: "blur" }
        ]
      }
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          post(AUTH().TokenAuth, this.loginForm)
            .then(response => {
              sessionStorage.setItem("token", response.data.token);
              sessionStorage.setItem("user_id", response.data.user_id);
              sessionStorage.setItem("user_name", response.data.user_name);
              this.$message({ message: "login successful", type: "success" });
              this.$emit("login");
              this.$router.push("/");
            })
            .catch(error => {
              this.$message({ message: error.data, type: "error" });
            });
        } else {
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    }
  }
};
</script>

<style scoped>
</style>
