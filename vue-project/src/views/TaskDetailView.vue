<template>
  <el-container class="layout-container">
    <!-- 左侧菜单 -->
    <NavBar/>
    <!-- 右侧主区域 -->
    <el-container>
      <el-header style="font-size: large; display: flex; justify-content: center; align-items: center;">
        任务详情
      </el-header>
      <el-card header="个人信息" shadow="never">
        <UserInformation current-page="task-detail"/>
      </el-card>
      <TaskDetail current-page="task-market-detail">
      </TaskDetail>

      <el-card shadow="never">
        <template #header>
          <span>子任务列表</span>&nbsp;&nbsp;
          <el-icon><Files /></el-icon>
        </template>
        <el-table
            size="large"
            :data="subTasks"
            stripe
            height="400px"
            style="width: 100%; max-height: 400px; overflow-y: auto;"
        >
          <el-table-column prop="subtask_index" label="子任务序号" />
          <el-table-column prop="content" label="内容">
            <template #default="scope" v-if="currentTask.data_type === '图片'">
              <el-image style="width: 100px; height: 100px" :src=scope.row.content :fit="'contain'" />
            </template>
          </el-table-column>
          <el-table-column prop="receiver" label="领取者" />
          <el-table-column prop="finish_time" label="完成时间" />
          <el-table-column prop="subtask_status" label="状态" />
          <el-table-column fixed="right" label="操作" width="300">
            <template #default="scope">
              <el-button
                  size="default"
                  type="warning"
                  :disabled="scope.row.receiver !== null"
                  @click="handleClaim(scope.row)"
              >
                {{ scope.row.receiver ? '已领取' : '领取' }}
              </el-button>
              <el-button
                  v-if="scope.row.subtask_status === '未完成' || scope.row.subtask_status === '未领取'"
                  size="default"
                  type="danger"
                  :disabled="scope.row.receiver !== currentUserName"
                  @click="handleAnnotateDrawer(scope.row)"
              >
                {{ canAnnotate(scope.row) ? '请标注' : '无需标注' }}
              </el-button>
              <el-button
                  v-else
                  size="default"
                  type="primary"
                  :disabled="scope.row.receiver !== currentUserName"
                  @click="viewResults(scope.row)"
              >
                查看结果
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-container>

    <!-- 添加抽屉组件 -->
    <el-drawer
        title="标注任务"
        v-model="drawerVisible"
        size="50%"
        :before-close="handleClose"
    >
      <!-- 抽屉内容，用于标注操作 -->
      <TaskAnnotation :subtask="currentSubTask" :current-task="currentTask"/>
    </el-drawer>
  </el-container>

  <el-dialog :show-close="false" v-model="dialogAnswerVisible" title="标注结果" width="800">
    <div v-if="currentTask.question_type === '框图题'">
      <image-framer-result :subtask="currentViewSubTask"></image-framer-result>
    </div>
    <div v-else>
      <h3>标注结果：{{ currentViewSubTask.answer }}</h3>
    </div>
    <el-button type="primary" @click="dialogAnswerVisible = false">返 回</el-button>
  </el-dialog>



</template>
<script setup>
import NavBar from '@/components/NavBar.vue' // 导入NavBar组件
import TaskAnnotation from "@/components/TaskAnnotation.vue";
import UserInformation from "@/components/UserInformation.vue";
import TaskDetail from "@/components/TaskDetail.vue";
import { ref,onMounted } from 'vue';
import axios from 'axios';
import {useRoute} from "vue-router";
import {Files} from "@element-plus/icons-vue";
import {ElMessage, ElMessageBox} from "element-plus";
import ImageFramerResult from "@/components/ImageFramerResult.vue";
const route = useRoute(); // 获取当前路由对象
const { task_id } = route.params; // 假设你的路由定义中包含了 task_id 参数
const currentTask = JSON.parse(sessionStorage.getItem("currentTask"));
// 假设这是从API获取的子任务数据 TODO 和后端修改
const subTasks = ref([]);

const fetchSubTasks = async () => {
  if (task_id) {
    try {
      // TODO url 请求地址修改 向后端查询对应任务ID的所有子任务列表，改成根据id和index查询？？
      const response = await axios.get(`http://127.0.0.1:8000/get_subtasks/`, {
        params: { task_id: task_id }
      });
      // 检查响应状态
      if (response.data.status === "ok") {
        // 将响应数据赋值给 subTasks 变量
        subTasks.value = response.data.data;

      } else {
        // 处理后端返回的错误状态
        console.error('获取子任务失败:', response.data.message);
        // 这里可以添加额外的错误处理逻辑，比如显示错误消息给用户
      }
    } catch (error) {
      console.error('请求子任务失败:', error);
    }
  }
};

onMounted(() =>{
  fetchSubTasks();
  const user = JSON.parse(sessionStorage.getItem('user'));
  currentUserId.value = user["user_id"];
  currentUserName.value =sessionStorage.getItem('username');
});



// 假设的当前用户ID
const currentUserId = ref(null); // 用实际的当前用户ID替换
const currentUserName = ref(''); // 用实际的当前用户名称替换
// 检查是否是当前用户且任务未完成



const handleClaim = (subtask) => {
  if (!subtask.receiver) {
    // 执行领取任务的逻辑
    const currentUser = sessionStorage.getItem('username');

    // 使用ElMessageBox.confirm来弹出确认对话框
    ElMessageBox.confirm('确定要领取此任务吗?', '领取任务', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
        .then(() => {
          // 用户点击“确定”，更新任务的receiver
          console.log('Claiming task:', subtask);
          // 调用函数更新后端任务状态
          updateTaskReceiver(subtask, currentUser).then(() => {
            // window.location.reload();
          }).catch((error) => {
            console.error('Failed to update task receiver:', error);
          });
        })
        .catch(() => {
          // 用户点击“取消”或关闭对话框时的操作
          console.log('Claiming task canceled by user.');
        });
  }
};
// 假设这是更新任务接收者状态的异步函数

// eslint-disable-next-line no-unused-vars
const updateTaskReceiver = async (subtask, receiver) => {
  try {
    console.log(subtask)
    // 构造请求体，包含所需的参数
    const data = {
      task_id: subtask.task, // 假设subtaskId对象包含taskId属性
      receiver: receiver,
      subtask_index:subtask.subtask_index
    };
    const header = {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
    };
    console.log(data)
    // TODO url 请求 发送POST请求到后端接口
    const response = await axios.post('http://127.0.0.1:8000/update_subtask_receiver/', data,header);
    console.log(response.data)
    // 检查响应状态
    if (response.data.status === 'ok') {
      // 更新成功
      ElMessage.success('子任务领取成功');
      subtask.receiver = receiver; // 这里直接修改了任务的receiver属性
      subtask.subtask_status = '未完成';
      // window.location.reload();
      return response.data;
    } else if (response.data.status === 'error') {
      // 更新失败，抛出错误信息
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    // 捕获并处理错误
    console.error('请求失败:', error);
  }
};

const canAnnotate = (task) => {
  return task.receiver === sessionStorage.getItem('username');
};
// 控制抽屉显示的响应式变量
const drawerVisible = ref(false);
const currentSubTask = ref(null);

// ... 省略其他代码 ...

// 处理标注任务的函数
const handleAnnotateDrawer = (task) => {
  if (canAnnotate(task)) {
    // 设置当前标注的子任务
    currentSubTask.value = task;
    // 显示抽屉
    drawerVisible.value = true;
  }
};

// 抽屉关闭前的回调函数
const handleClose = (done) => {
  // 可以在这里执行一些清理操作，例如重置表单数据
  done(); // 调用 done 以关闭抽屉
};

const dialogAnswerVisible =ref(false)
const currentViewSubTask =ref(null)
function viewResults(subtask){
  dialogAnswerVisible.value=true
  if (subtask.answer === "" || subtask.answer === null){
    subtask.answer="[]";
  }
  currentViewSubTask.value = JSON.parse(JSON.stringify(subtask));
  console.log(currentViewSubTask.value)
  currentViewSubTask.value.answer = JSON.parse(currentViewSubTask.value.answer)
}

</script>
<style scoped lang="scss">
</style>