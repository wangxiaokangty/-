<template>
  <!--  element plus的容器-->
  <el-container class="layout-container">
    <!-- 左侧菜单 -->
    <NavBar/>
    <!-- 右侧主区域 -->
    <el-container>
      <el-header style="font-size: large; display: flex; justify-content: center; align-items: center;">
        被举报任务列表
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
        <el-table :data="subTasks" height="500">
          <el-table-column prop="subtask_id" label="子任务ID" />
          <el-table-column prop="content" label="内容">
            <template #default="scope" v-if="currentSubTaskType === '图片'">
              <el-image style="width: 100px; height: 100px" :src=scope.row.content :fit="'contain'" />
            </template>
          </el-table-column>
          <el-table-column prop="subtask_status" label="当前状态" />
          <el-table-column prop="answer" label="标注结果" v-if="currentQuestionType!=='框图题'" />
          <el-table-column label="标注结果" v-if="currentQuestionType==='框图题'">
            <template #default="scope">
              <el-button size="large" @click="viewImageAnswer(scope.row)" :disabled="scope.row.subtask_status==='未完成' || scope.row.subtask_status==='未领取'">
                查看详情
              </el-button>
            </template>
          </el-table-column>
          <!-- 根据需要添加更多列 -->
          <!-- 在el-table中添加按钮列 -->
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="success" size="default" @click="handleReportSuccess(scope.row)">举报成功</el-button>
              <el-button type="danger" size="default" @click="handleReportFailure(scope.row)">举报失败</el-button>
            </template>
          </el-table-column>
        </el-table>
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
//import UserInformation from "@/components/UserInformation.vue";
import axios from 'axios';
import {ref, onMounted} from 'vue';
import {Files} from "@element-plus/icons-vue";
import { CircleCloseFilled } from '@element-plus/icons-vue'
const tasks = ref([]);

// 请求任务数据的函数
async function fetchTasks() {
  const params = {
    subtask_status:"举报中"
  }
  try {
    // TODO url 修改请求地址
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
    // TODO url 修改请求地址
    const response = await axios.get(`http://127.0.0.1:8000/get_subtasks/`, { params: { task_id: task.task_id,subtask_status:'举报中'} });
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
}
function viewImageAnswer(subtask) {
  dialogImageVisible.value = true;
  if (subtask.answer === null || subtask.answer === ""){
    subtask.answer="[]";
  }
  currenSubTask.value = subtask;
  currenSubTask.value.answer = JSON.parse(currenSubTask.value.answer)
}

// 处理举报成功的函数
import {ElMessage, ElMessageBox} from 'element-plus';

function handleReportSuccess(subtask) {
  // 构造请求数据
  const reportData = {
    task_id: subtask.task,
    subtask_index: subtask.subtask_index, // 确保你有subtask_index字段
    approvalStatus: 'true', // 举报成功，设置为true
  };

  // 构造请求头部
  const header = {
    'Content-Type': 'application/x-www-form-urlencoded'
  };

  // 发送请求到后端
  axios.post('http://127.0.0.1:8000/process_report/', reportData, { headers: header })
      .then(response => {
        if (response.data.status === 'ok') {
          // 举报成功后弹出确认框
          ElMessageBox.confirm('处理成功', '提示', {
            confirmButtonText: '确定',
            type: 'success',
            callback: action => {
              if (action === 'confirm') {
                // 用户点击确定后的操作，比如刷新页面
                window.location.reload();
              }
            }
          });
        } else {
          // 处理错误情况
          console.error('处理失败:', response.data.message);
          ElMessage.error('处理失败: ' + response.data.message);
        }
      })
      .catch(error => {
        console.error('请求失败:', error);
        ElMessage.error('请求失败: ' + error.message);
      });
}

function handleReportFailure(subtask) {
  // 构造请求数据
  const reportData = {
    task_id: subtask.task,
    subtask_index: subtask.subtask_index, // 确保你有subtask_index字段
    approvalStatus: 'false', // 举报失败，设置为false
  };

  // 构造请求头部
  const header = {
    'Content-Type': 'application/x-www-form-urlencoded'
  };

  // 发送请求到后端
  axios.post('http://127.0.0.1:8000/process_report/', reportData, { headers: header })
      .then(response => {
        if (response.data.status === 'ok') {
          // 举报失败后弹出确认框
          ElMessageBox.alert('处理成功！', '提示', {
            confirmButtonText: '确定',
            type: 'error',
          }).then(() => {
            // 用户点击确定后的操作，比如刷新子任务列表
            window.location.reload();
          });
        } else {
          // 处理错误情况
          ElMessage.error('处理失败: ' + response.data.message);
        }
      })
      .catch(error => {
        ElMessage.error('请求失败: ' + error.message);
      });
}
</script>

<style scoped lang="scss">
.task-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* 可根据需要添加上边距 */
}
</style>