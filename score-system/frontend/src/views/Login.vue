<template>
  <div class="login-page">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <span>成绩登记系统</span>
        </div>
      </template>
      <el-form :model="form" @submit.prevent="handleLogin">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin">登录</el-button>
          <el-button @click="showRegister = true">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-dialog v-model="showRegister" title="注册账号">
      <el-form :model="registerForm">
        <el-form-item label="用户名">
          <el-input v-model="registerForm.username" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="registerForm.password" type="password" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="registerForm.name" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="registerForm.role">
            <el-option label="学生" value="student" />
            <el-option label="教师" value="teacher" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRegister = false">取消</el-button>
        <el-button type="primary" @click="handleRegister">注册</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';
import { authAPI } from '../api';
import { ElMessage } from 'element-plus';

const router = useRouter();
const auth = useAuthStore();
const form = ref({ username: '', password: '' });
const registerForm = ref({ username: '', password: '', name: '', role: 'student' });
const showRegister = ref(false);

const handleLogin = async () => {
  try {
    const { data } = await authAPI.login(form.value.username, form.value.password);
    auth.login(data.token, data.user);
    router.push('/dashboard');
  } catch {
    ElMessage.error('登录失败');
  }
};

const handleRegister = async () => {
  try {
    await authAPI.register(registerForm.value);
    ElMessage.success('注册成功，请登录');
    showRegister.value = false;
  } catch {
    ElMessage.error('注册失败');
  }
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f5f7fa;
}
.login-card {
  width: 400px;
}
</style>
