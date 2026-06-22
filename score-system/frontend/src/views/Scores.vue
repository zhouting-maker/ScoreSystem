<template>
  <div>
    <el-button type="primary" @click="showDialog = true" v-if="auth.user.role === 'teacher'">
      新增成绩
    </el-button>
    <el-button @click="handleExport" v-if="auth.user.role === 'teacher'">导出 Excel</el-button>

    <el-table :data="scores" style="margin-top: 20px">
      <el-table-column prop="student_no" label="学号" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="course_name" label="课程" />
      <el-table-column prop="score" label="成绩" />
    </el-table>

    <el-dialog v-model="showDialog" title="新增成绩">
      <el-form :model="form">
        <el-form-item label="学生">
          <el-select v-model="form.student_id">
            <el-option v-for="s in students" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="课程">
          <el-select v-model="form.course_id">
            <el-option v-for="c in courses" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="成绩">
          <el-input-number v-model="form.score" :min="0" :max="100" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../store/auth';
import { scoreAPI, adminAPI } from '../api';
import { ElMessage } from 'element-plus';

const auth = useAuthStore();
const scores = ref([]);
const students = ref([]);
const courses = ref([]);
const showDialog = ref(false);
const form = ref({ student_id: '', course_id: '', score: '' });

onMounted(async () => {
  await loadScores();
  if (auth.user.role === 'teacher') {
    await Promise.all([
      adminAPI.getStudents().then(r => students.value = r.data),
      adminAPI.getCourses().then(r => courses.value = r.data)
    ]);
  }
});

const loadScores = async () => {
  const { data } = await scoreAPI.getScores();
  scores.value = data;
};

const handleSubmit = async () => {
  try {
    await scoreAPI.addScore(form.value);
    ElMessage.success('保存成功');
    showDialog.value = false;
    form.value = { student_id: '', course_id: '', score: '' };
    await loadScores();
  } catch {
    ElMessage.error('保存失败');
  }
};

const handleExport = async () => {
  try {
    const { data } = await scoreAPI.exportExcel();
    const url = window.URL.createObjectURL(new Blob([data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'scores.xlsx');
    link.click();
  } catch {
    ElMessage.error('导出失败');
  }
};
</script>
