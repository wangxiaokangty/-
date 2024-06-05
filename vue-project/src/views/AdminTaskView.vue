<template>
  <!--  element plus的容器-->
  <el-container class="layout-container">
    <!-- 左侧菜单 -->
    <NavBar/>
    <!-- 右侧主区域 -->
    <el-container>
      <el-header style="font-size: large; display: flex; justify-content: center; align-items: center;">
        待审核任务
      </el-header>

      <el-card shadow="never">
        <template #header>
          <span>已发布任务列表</span>&nbsp;&nbsp;
          <el-icon><Files /></el-icon>
        </template>
        <el-table
            size="large"
            :data="tasks"
            stripe
            height="400px"
            style="width: 100%; max-height: 400px; overflow-y: auto;"
        >
          <el-table-column prop="task_id"  label="任务ID" />
          <el-table-column prop="publisher" label="发布者"/>
          <el-table-column prop="task_name" label="任务名称"/>
          <el-table-column prop="data_type" label="数据类型"/>
          <el-table-column prop="question_type" label="问题类型"/>
          <el-table-column prop="task_status" label="当前状态"/>
          <el-table-column label="查看详情">
            <template #default="scope">
              <el-button size="large" @click="showSubTasksDrawer(scope.row)">
                点击查看详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-container>
  </el-container>


  <!-- 添加抽屉 -->
  <el-drawer
      title="子任务详情"
      v-model="subTasksDrawerVisible"
      size="70%"
      :show-close="false"
  >
    <template #header="{ close, titleId, titleClass }">
      <h4 :id="titleId" :class="titleClass">子任务列表</h4>
      <el-button type="danger" @click="close">
        <el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>
        Close
      </el-button>
    </template>
    <div v-if="subTasksDrawerVisible">
      <!-- 子任务列表 -->
      <TaskDetail current-page="posted-task"/>
      <el-card shadow="never">
        <el-table :data="subTasks" height="300">
          <el-table-column prop="subtask_index" label="子任务索引" />
          <el-table-column prop="content" label="内容">
            <template #default="scope" v-if="currentSubTaskType === '图片'">
              <el-image style="width: 100px; height: 100px" :src=scope.row.content :fit="'contain'" />
            </template>
          </el-table-column>
          <el-table-column prop="subtask_status" label="当前状态" />
          <!-- 根据需要添加更多列 -->
        </el-table>
      </el-card>
      <el-card shadow="never">
        <!-- 添加表单 -->
        <el-form :model="form" @submit.prevent="handleSubmit">
          <el-form-item label="审核结果">
            <el-radio-group v-model="form.approvalStatus">
              <el-radio :label="true">通过</el-radio>
              <el-radio :label="false">不通过</el-radio>
            </el-radio-group>
          </el-form-item>
          <template v-if="!form.approvalStatus">
            <el-form-item label="不通过理由">
              <el-input type="textarea" v-model="form.rejectionReason"></el-input>
            </el-form-item>
          </template>
          <el-form-item>
            <el-button type="primary" @click="handleSubmit">提交审核</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </el-drawer>

  <el-dialog :show-close="false" v-model="dialogImageVisible" title="标注结果" width="800" >
    <image-framer-result :subtask="currenSubTask"></image-framer-result>
    <el-button type="primary" @click="dialogImageVisible = false">返 回</el-button>
  </el-dialog>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue';
import TaskDetail from "@/components/TaskDetail.vue";
import ImageFramerResult from "@/components/ImageFramerResult.vue";
import axios from 'axios';
import {ref, onMounted} from 'vue';
import {Files} from "@element-plus/icons-vue";
import { CircleCloseFilled } from '@element-plus/icons-vue'
import {ElMessage} from "element-plus";
const tasks = ref([]);

// 请求任务数据的函数
async function fetchTasks() {
  const params = {
    task_status:"审核中"
  }
  try {
    // TODO url 修改后端请求地址
    const response = await axios.get('http://127.0.0.1:8000/get_tasks/',{params:params});
    tasks.value = response.data["data"];
  } catch (error) {
    console.error('请求任务数据失败：', error);
  }
}

// 组件挂载后请求数据
onMounted(() => {
  fetchTasks();
});


// 控制抽屉的显示和隐藏
const currentSubTaskType = ref('')
const currentQuestionType = ref('')
const subTasksDrawerVisible = ref(false);
// 子任务数据
const subTasks = ref([]);
const currentTask =ref(Object)

const dialogImageVisible = ref(false)
const currenSubTask = ref(null)
// 获取子任务数据的函数
async function fetchSubTasks(task) {
  try {
    currentSubTaskType.value = task.data_type;
    currentQuestionType.value = task.question_type;
    // TODO 修改后端请求地址
    const response = await axios.get(`http://127.0.0.1:8000/get_subtasks/`, { params: { task_id: task.task_id } });
    subTasks.value = response.data["data"];
  } catch (error) {
    console.error('请求子任务数据失败：', error);
  }
}
// 显示子任务抽屉的函数
function showSubTasksDrawer(task) {
  fetchSubTasks(task); // 获取子任务数据
  currentTask.value=task;
  subTasksDrawerVisible.value = true; // 显示抽屉
  sessionStorage.setItem("currentTaskId",task.task_id);
  form.value = {
    approvalStatus: true, // 默认为“通过”
    rejectionReason: '' // 不通过理由
  }
}
// 表单数据
const form = ref({
  approvalStatus: true, // 默认为“通过”
  rejectionReason: '' // 不通过理由
});

// 提交表单的函数
async function handleSubmit() {
  try {
    const data = {
      task_id: currentTask.value.task_id,
      approvalStatus: form.value.approvalStatus,
      rejectionReason: form.value.rejectionReason
    };
    const header = {
      'Content-Type': 'application/x-www-form-urlencoded'
    };
    // TODO 修改后端请求地址
    const response = await axios.post('http://127.0.0.1:8000/admin_submit_review/', data,{ headers: header });
    // 处理响应
    // 根据响应显示消息提示
    if (response.data.status === 'ok') {
      // 审核结果提交成功
      ElMessage.success(response.data.message);
      subTasksDrawerVisible.value = false; // 关闭抽屉
      window.location.reload();
    } else {
      // 审核结果提交失败
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    // 网络或其他错误，显示错误消息
    ElMessage.error('提交审核失败，请稍后重试。');
    console.error('提交审核失败：', error);
  }
}

</script>

<style scoped lang="scss">
.task-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* 可根据需要添加上边距 */
}
</style>