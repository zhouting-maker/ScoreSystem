<template>
  <div class="dashboard">
    <el-header class="header">
      <div>欢迎，{{ auth.user.name }} ({{ auth.user.role }})</div>
      <el-button type="danger" @click="handleLogout">退出</el-button>
    </el-header>
    <el-container>
      <el-aside>
        <el-menu :default-active="active" @select="handleMenuSelect">
          <el-menu-item index="scores">成绩管理</el-menu-item>
          <el-menu-item index="report" v-if="['teacher', 'admin'].includes(auth.user.role)">统计报表</el-menu-item>
          <el-menu-item index="admin" v-if="auth.user.role === 'admin'">系统管理</el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <component :is="currentView" />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';
import Scores from './Scores.vue';
import Report from './Report.vue';
import Admin from './Admin.vue';

const router = useRouter();
const auth = useAuthStore();
const active = ref('scores');

const currentView = computed(() => {
  const views = { scores: Scores, report: Report, admin: Admin };
  return views[active.value] || Scores;
});

const handleMenuSelect = (index) => {
  active.value = index;
};

const handleLogout = () => {
  auth.logout();
  router.push('/login');
};
</script>

<style scoped>
.dashboard {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.header {
  background: #409eff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}
.el-container {
  flex: 1;
}
.el-aside {
  width: 200px;
  background: #f5f7fa;
}
</style>
