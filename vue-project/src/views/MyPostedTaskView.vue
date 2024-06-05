<template>
  <!--  element plus的容器-->
  <el-container class="layout-container">
    <!-- 左侧菜单 -->
    <NavBar/>
    <!-- 右侧主区域 -->
    <el-container>
      <el-header style="font-size: large; display: flex; justify-content: center; align-items: center;">
        已发布任务
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
          <el-table-column prop="deadline_time" label="截止日期"/>
          <el-table-column prop="each_pay" label="报酬"/>
          <el-table-column prop="task_status" label="当前状态"/>
          <el-table-column label="Operations">
            <template #default="scope">
              <el-button size="large" @click="showSubTasksDrawer(scope.row)" v-if="checkApprovalStatus(scope.row.task_status)">
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
        <el-table-column prop="subtask_index" label="子任务索引" />
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
        <!-- 反馈任务按钮 -->
        <el-table-column label="反馈任务">
          <template #default="scope">
            <!-- 根据 status 显示不同的按钮 -->
            <div v-if="scope.row.subtask_status === '举报中'">
              <el-button size="large" disabled type="warning">举报中</el-button>
            </div>
            <div v-else-if="scope.row.subtask_status === '举报已解决'">
              <el-button size="large" disabled type="success">举报已解决</el-button>
            </div>
            <div v-else-if="scope.row.subtask_status === '已完成'">
              <el-button size="large" @click="reportSubtask(scope.row)" type="primary">
                举报
              </el-button>
            </div>
            <div v-else>
              <el-button size="large" disabled type="danger">任务未完成</el-button>
            </div>
          </template>
        </el-table-column>
        <!-- 根据需要添加更多列 -->
      </el-table>

      </el-card>
      <div class="task-actions">
        <!-- 根据任务状态显示不同的按钮 -->
        <el-button
            size="large"
            :type="currentTask.task_status === '进行中' ? 'danger' : 'primary'"
            @click="currentTask.task_status === '进行中' ? confirmEndTask() : downloadData()"
        >
          {{ currentTask.task_status === '进行中' ? '终止任务' : '下载数据' }}
        </el-button>
      </div>
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
import {ElMessage} from "element-plus";
const tasks = ref([]);

// 请求任务数据的函数
async function fetchTasks() {
  const params = {
    publisher: sessionStorage.getItem("username")
  }
  try {
    // TODO url 请求地址修改
    const response = await axios.get('http://127.0.0.1:8000/get_tasks/',{params:params});
    if (response.data.status==="ok") {
      tasks.value = response.data["data"];
    } else if (response.data.status==="error") {
      ElMessage.error(response.data["message"])
    }
  } catch (error) {
    ElMessage.error('请求任务数据失败')
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
// 获取子任务数据的函数
async function fetchSubTasks(task) {
  try {
    currentSubTaskType.value = task.data_type;
    currentQuestionType.value = task.question_type;
    // TODO url 修改请求地址
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
}

function reportSubtask(subTask) {
  // 构建举报数据
  const data = {
    task_id: subTask.task,
    subtask_index: subTask.subtask_index
  };
  console.log(subTask)
  const header = {
    headers : {"Content-Type": "application/x-www-form-urlencoded"}
  };
  // TODO url 发送举报请求
  axios.post('http://127.0.0.1:8000/report_subtask/', data, header)
      .then(response => {
        // 根据后端返回的状态码处理不同的逻辑
        if (response.data.status === 'ok') {
          // 举报成功，显示成功消息
          ElMessage.success(response.data.message);
          subTask.subtask_status = "举报中";
        } else {
          // 举报失败，显示错误消息
          ElMessage.error(response.data.message);
        }
      })
      .catch(error => {
        // 网络或其他错误，显示错误消息
        ElMessage.error('因为网络原因，举报任务失败，请稍后重试。');
        console.error('举报任务失败：', error);
      });
}

function confirmEndTask() {
  // 弹出确认框
  const confirmEnd = window.confirm('确定要终止任务吗？');
  if (confirmEnd) {
    // 如果用户确认，调用 API 终止任务
    endTask().then((response) => {
      // 终止任务成功后的逻辑
      if (response.data.status==="ok") {
        ElMessage.success(response.data.message);
        currentTask.value.task_status = "提前终止"
      } else if (response.data.status==="error") {
        ElMessage.error(response.data.message);
      }
    }).catch((error) => {
      // 处理错误
      console.error('终止任务失败：', error);
    });
  }
}

async function endTask() {
  console.log(currentTask)
  const data = {
    task_id: Number(sessionStorage.getItem('currentTaskId')),
    type: "提前终止"
  };
  const header = {
    headers : {"Content-Type": "application/x-www-form-urlencoded"}
  };
  // eslint-disable-next-line no-useless-catch
  try {
    // TODO url 修改请求地址
    const response = await axios.post('http://127.0.0.1:8000/terminate_task/', data, header);
    // 处理响应
    return response;
  } catch (error) {
    // 这里可以抛出错误，让调用者处理
    throw error;
  }
}
const dialogImageVisible = ref(false)
const currenSubTask = ref(null)
function viewImageAnswer(subtask) {
  dialogImageVisible.value = true;
  if (subtask.answer === null || subtask.answer === ""){
    subtask.answer="[]";
  }
  currenSubTask.value = subtask;
  currenSubTask.value.answer = JSON.parse(currenSubTask.value.answer)
}

// 下载数据的函数
function downloadData() {
  console.log(subTasks.value)

  const columns = ['子任务ID', '内容', '标注结果']; // 添加列名
  let csvContent = columns.join(',') + '\n'; // 开始 CSV 内容，包含列名

  // 过滤出需要的字段并追加到 CSV 格式
  csvContent += subTasks.value
      .map(subTask => {
        // 检查当前任务的数据类型是否为图片
        if (currentSubTaskType.value === '文本') {
          // 如果是文本类型，返回完整文本内容
          return [
            subTask.subtask_index,
            subTask.content,
            subTask.answer,
          ];
        } else {
          // 如果是其他类型，返回文件名
          const fileName = subTask.content.split('/').pop(); // 获取路径中的文件名
          return [
            subTask.subtask_id,    // 子任务 ID
            fileName,      // 使用文件名替代完整内容
            subTask.answer,  // 标注结果
          ];
        }
      })
      .map(row => row.join(',')) // 将每个子数组的元素用逗号连接
      .join('\n'); // 用换行符将每一行连接起来

  // 创建 Blob 对象
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });

  // 创建下载链接
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `task-${currentTask.value.task_name}_subtasks_utf8.csv`); // 指定下载文件的名称
  document.body.appendChild(link); // 将链接添加到文档
  link.click(); // 触发下载
  document.body.removeChild(link); // 下载后移除链接
}
const checkApprovalStatus = (status) => {
  return !(status === "审核中" || status === "审核未通过");
}
</script>

<style scoped lang="scss">
.task-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* 可根据需要添加上边距 */
}
</style>