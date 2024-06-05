<template>
  <!--  element plus的容器-->
  <el-container class="layout-container">
    <!-- 左侧菜单 -->
    <NavBar/>
    <!-- 右侧主区域 -->
    <el-container>
      <el-header style="font-size: large; display: flex; justify-content: center; align-items: center;">
        任务广场
      </el-header>
      <el-card header="个人信息" shadow="never">
        <UserInformation current-page="task-market"/>
      </el-card>

      <el-card shadow="never">
        <template #header>
          <span>您已领取的任务列表如下</span>&nbsp;&nbsp;
          <el-icon><Files /></el-icon>
        </template>
        <el-table
            size="large"
            :data="tasks"
            default-sort="{ prop: 'deadline_time', order: 'descending' }"
            stripe
            height="400px"
            style="width: 100%; max-height: 400px; overflow-y: auto;"
        >
          <el-table-column prop="task_id"  label="任务ID" />
          <el-table-column prop="publisher" label="发布者"/>
          <el-table-column prop="task_name" label="任务名称"/>
          <el-table-column prop="data_type" sortable label="数据类型"/>
          <el-table-column prop="question_type" sortable label="问题类型"/>
          <el-table-column prop="deadline_time" sortable label="截止日期"/>
          <el-table-column prop="each_pay" label="报酬"/>
          <el-table-column prop="task_status" sortable label="当前状态"/>
          <el-table-column label="Operations">
            <template #default="scope">
              <el-button
                  size="large"
                  @click="viewTaskDetail(scope.row)"
                  :disabled="checkTaskDeadline(scope.row.deadline_time,scope.row.task_status)"
              >
                {{ checkTaskDeadline(scope.row.deadline_time,scope.row.task_status) ? '任务已截止' : '查看详情' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-container>
  </el-container>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue';
import UserInformation from "@/components/UserInformation.vue";
import axios from 'axios';
import {ref, onMounted} from 'vue';
import {Files} from "@element-plus/icons-vue";
import router from "@/router";
import dayjs from 'dayjs';
const tasks = ref([]);


async function fetchTasks() {
  try {
    // TODO url 修改后端请求 和后端修改 请求任务数据的函数
    const response = await axios.get('http://127.0.0.1:8000/get_tasks/',{params:{receiver:sessionStorage.getItem("username")}});
    tasks.value = response.data["data"];
  } catch (error) {
    console.error('请求任务数据失败：', error);
  }
}

function viewTaskDetail(task) {
  router.push({ name: 'task-detail', params: { task_id: task.task_id} });
  sessionStorage.setItem("currentTaskId",task.task_id);
  sessionStorage.setItem("currentTask",JSON.stringify(task));
  sessionStorage.setItem("currentTaskDataType",task.data_type)
}

const checkTaskDeadline = (deadline_time,status) => {
  const taskDeadline = dayjs(deadline_time);
  if (status === "提前终止") {
    return true;
  }
  return dayjs().isAfter(taskDeadline, 'day');
};
// 组件挂载后请求数据
onMounted(() => {
  fetchTasks();
});
</script>

<style scoped lang="scss">

</style>