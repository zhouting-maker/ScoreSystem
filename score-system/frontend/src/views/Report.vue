<template>
  <div>
    <el-table :data="report">
      <el-table-column prop="name" label="课程" />
      <el-table-column prop="avg_score" label="平均分" :formatter="formatScore" />
      <el-table-column prop="max_score" label="最高分" />
      <el-table-column prop="min_score" label="最低分" />
      <el-table-column prop="total" label="人数" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { scoreAPI } from '../api';

const report = ref([]);

onMounted(async () => {
  const { data } = await scoreAPI.getReport();
  report.value = data;
});

const formatScore = (row) => row.avg_score ? row.avg_score.toFixed(2) : '-';
</script>
