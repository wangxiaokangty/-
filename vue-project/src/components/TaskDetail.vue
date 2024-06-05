<template>
  <!-- 确保 currentPage 匹配时才渲染组件 -->
  <el-card header="任务详情" shadow="never" v-if="props.currentPage === 'task-market-detail'">
    <el-descriptions size="large" border column="4">
      <!-- 使用 task 实例的数据填充 el-descriptions-item -->
      <el-descriptions-item label="任务名称">{{ task?.task_name }}</el-descriptions-item>
      <el-descriptions-item label="任务星级">{{ task?.task_rank }}</el-descriptions-item>
      <el-descriptions-item label="任务数量">{{ task?.data_nums }}</el-descriptions-item>
      <el-descriptions-item label="截止日期">{{ task?.deadline_time }}</el-descriptions-item>
      <el-descriptions-item label="数据类型">{{ task?.data_type }}</el-descriptions-item>
      <el-descriptions-item label="问题类型">{{ task?.question_type }}</el-descriptions-item>
      <el-descriptions-item label="报酬">{{ task?.each_pay }}</el-descriptions-item>
      <el-descriptions-item label="当前状态">{{ task?.task_status }}</el-descriptions-item>
      <el-descriptions-item label="任务描述">{{ task?.task_description }}</el-descriptions-item>
    </el-descriptions>
  </el-card>

  <el-card header="任务详情" shadow="never" v-if="props.currentPage === 'posted-task'">
    <el-descriptions size="large" border column="3">
      <!-- 使用 task 实例的数据填充 el-descriptions-item -->
      <el-descriptions-item label="任务名称">{{ task?.task_name }}</el-descriptions-item>
      <el-descriptions-item label="任务数量">{{ task?.data_nums }}</el-descriptions-item>
      <el-descriptions-item label="截止日期">{{ task?.deadline_time }}</el-descriptions-item>
      <el-descriptions-item label="数据类型">{{ task?.data_type }}</el-descriptions-item>
      <el-descriptions-item label="问题类型">{{ task?.question_type }}</el-descriptions-item>
      <el-descriptions-item label="当前状态">{{ task?.task_status }}</el-descriptions-item>
    </el-descriptions>
  </el-card>
</template>

<script setup>
import {defineProps, onMounted, ref} from 'vue';
import axios from 'axios';
import {ElMessage} from "element-plus";

// 定义组件的 props
const props = defineProps({
  currentPage: String,
});

// 创建响应式变量来存储 task 数据
const task = ref(null);

onMounted(()=>{
  const taskid = Number(sessionStorage.getItem('currentTaskId'))
  fetchTask(taskid)
})
// TODO 假设 fetchTask 函数用于获取任务详情
// 这个函数会在组件加载时被调用
async function fetchTask(taskID) {
  try {
    //TODO url 修改后端请求地址
    const response = await axios.get('http://127.0.0.1:8000/get_tasks/', { params: {task_id:taskID}});
    if (response.data["status"] === "ok") {
      task.value = response.data["data"][0];
    } else if (response.data["status"] === "error") {
      if (response.data["message"]){
        ElMessage.error(response.data["message"])
      } else{
        ElMessage.error('查询任务失败')
      }
    }

  } catch (error) {
    console.error('请求任务数据失败：', error);
  }
}
</script>
<style scoped lang="scss">

</style>