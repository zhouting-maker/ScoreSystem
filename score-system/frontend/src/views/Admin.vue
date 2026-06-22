<template>
  <div>
    <el-tabs>
      <el-tab-pane label="用户管理">
        <el-table :data="users">
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="role" label="角色" />
          <el-table-column label="操作">
            <template #default="{ row }">
              <el-button type="danger" @click="deleteUser(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="学生管理">
        <el-button type="primary" @click="showStudentDialog = true">新增学生</el-button>
        <el-table :data="students" style="margin-top: 20px">
          <el-table-column prop="student_no" label="学号" />
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="class_name" label="班级" />
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="成绩上报">
        <el-button type="success" @click="handlePublishEDU">上报教育部</el-button>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="showStudentDialog" title="新增学生">
      <el-form :model="studentForm">
        <el-form-item label="学号">
          <el-input v-model="studentForm.student_no" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="studentForm.name" />
        </el-form-item>
        <el-form-item label="班级">
          <el-input v-model="studentForm.class_name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showStudentDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAddStudent">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { adminAPI } from '../api';
import { ElMessage } from 'element-plus';

const users = ref([]);
const students = ref([]);
const showStudentDialog = ref(false);
const studentForm = ref({ student_no: '', name: '', class_name: '' });

onMounted(async () => {
  await Promise.all([
    adminAPI.getUsers().then(r => users.value = r.data),
    adminAPI.getStudents().then(r => students.value = r.data)
  ]);
});

const deleteUser = async (id) => {
  try {
    await adminAPI.deleteUser(id);
    ElMessage.success('删除成功');
    users.value = users.value.filter(u => u.id !== id);
  } catch {
    ElMessage.error('删除失败');
  }
};

const handleAddStudent = async () => {
  try {
    await adminAPI.addStudent(studentForm.value);
    ElMessage.success('添加成功');
    showStudentDialog.value = false;
    const { data } = await adminAPI.getStudents();
    students.value = data;
  } catch {
    ElMessage.error('添加失败');
  }
};

const handlePublishEDU = async () => {
  try {
    const { data } = await adminAPI.publishEDU();
    ElMessage.success(`成功上报 ${data.recordCount} 条记录`);
  } catch {
    ElMessage.error('上报失败');
  }
};
</script>
