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
          <span>任务列表</span>&nbsp;&nbsp;
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
                  :disabled="checkTaskDeadline(scope.row)"
                  v-if="checkApprovalStatus(scope.row.task_status)"
              >
                {{ checkTaskDeadline(scope.row) ? '任务已截止' : '查看详情' }}
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
    // TODO url 修改后端请求地址 和后端修改 请求任务数据的函数
    const response = await axios.get('http://127.0.0.1:8000/get_tasks/');
    // 检查响应状态
    if (response.data.status === "ok") {
      // 将响应数据中的 task 数据赋值给 tasks 变量
      tasks.value = response.data.data;
      // 处理逾期任务
      await handleOverdueTasks();
    } else {
      // 处理后端返回的错误状态
      console.error('获取任务失败:', response.data.message);
      // 这里可以添加额外的错误处理逻辑，比如显示错误消息给用户
    }
  } catch (error) {
    console.error('请求任务数据失败：', error);
  }
}
// 处理逾期任务的函数
async function handleOverdueTasks() {
  const now = dayjs(); // 获取当前时间
  tasks.value.forEach(task => {
    const taskDeadline = dayjs(task.deadline_time);
    task.options = JSON.parse(task.options)
    if (now.isAfter(taskDeadline, 'day') && task.task_status === "进行中") {
      // 如果任务已逾期且在进行中，则发起终止请求
      terminateTask(task);
      task.task_status="已逾期"
    }
  });
}

// 发起终止任务的请求
async function terminateTask(task) {
  try {
    const postData = {
      "task_id": task.task_id,
      "type": "已逾期"
    };
    const header = {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
    }
    // TODO url 修改请求地址
    const response = await axios.post('http://127.0.0.1:8000/terminate_task/', postData,header);
    if (response.data.status === 'ok') {
      console.log(`任务${task.task_id}逾期处理成功`);
      // 这里可以更新前端的任务状态显示
      // 例如，将任务状态更新为"已逾期"
    } else {
      console.error(`任务${task.task_id}逾期处理失败: ${response.data.message}`);
    }
  } catch (error) {
    console.error(`请求失败: ${error}`);
  }
}




function viewTaskDetail(task) {
  router.push({ name: 'task-detail', params: { task_id: task.task_id} });
  sessionStorage.setItem("currentTaskId",task.task_id);
  sessionStorage.setItem("currentTask",JSON.stringify(task));
  sessionStorage.setItem("currentTaskDataType",task.data_type)
}

const checkTaskDeadline = (task) => {
  const taskDeadline = dayjs(task.deadline_time);
  if (task.task_status === "提前终止") {
    return true;
  }
  return dayjs().isAfter(taskDeadline, 'day');
};

const checkApprovalStatus = (status) => {
  return !(status === "审核中" || status === "审核未通过");
}
// 组件挂载后请求数据
onMounted(() => {
  fetchTasks();
});
</script>

<style scoped lang="scss">

</style>