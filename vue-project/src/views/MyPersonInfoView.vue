<template>
  <el-container class="layout-container">
    <!-- 左侧菜单 -->
    <NavBar />
    <!-- 右侧主区域 -->
    <el-container>
      <el-header style="font-size: large; display: flex; justify-content: center; align-items: center;">
        个人信息
      </el-header>
      <el-card shadow="never" style="margin: auto;width: 60%;">
          <div class="form-container">
            <el-form :model="user" @submit.prevent="submitForm" label-width="100px">
              <!-- 将前四个 el-form-item 放在这里 -->
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="用户名">
                    <el-input v-model="user.username"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="邮箱">
                    <el-input v-model="user.email" disabled></el-input>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="余额">
                    <el-input v-model="user.userBalance" disabled></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="信用等级">
                    <el-input v-model="user.userCreditRank" disabled></el-input>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="当前经验">
                    <el-input v-model="user.userCurrentExp" disabled></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="升级须达到">
                    <el-input v-model="upEXP" disabled></el-input>
                  </el-form-item>
                </el-col>
              </el-row>
              <!-- 其他 el-form-item -->
              <el-form-item>
                <el-button type="primary" @click="submitForm" disabled>保存更改</el-button>
              </el-form-item>
            </el-form>
          </div>
      </el-card>
      <el-card shadow="never" style="margin: auto;width: 60%;">
        <el-form label-width="100px">
          <el-form-item label="余额">
            <el-input v-model="user.userBalance" readonly></el-input>
          </el-form-item>
          <el-form-item label="充值金额">
            <el-input v-model="rechargeAmount" placeholder="请输入充值金额"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleRecharge">充值</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card shadow="never" style="width: 60%; margin: auto;">
        <el-table :data="messages" style="width: 100%" height="350">
          <el-table-column prop="id" label="ID" width="100"></el-table-column>
          <el-table-column prop="time" label="时间" sortable></el-table-column>
          <el-table-column prop="sender" label="发送者"></el-table-column>
          <el-table-column prop="task_id" label="任务id"></el-table-column>
          <el-table-column prop="subtask_id" label="子任务id"></el-table-column>
          <el-table-column prop="content" label="内容"></el-table-column>
        </el-table>
      </el-card>
    </el-container>
  </el-container>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';
import { ref,onMounted } from 'vue';
import { ElMessage } from 'element-plus';

// 用户数据的响应式引用
const user = ref({
  user_id: 0,
  username: '',
  email: '',
  userBalance: 0,
  userCreditRank: 0,
  userCurrentExp: 0,
});
const upEXP=ref(0)
let dictionary = {
  "1": 100,
  "2": 500,
  "3": 1000,
  "4": 2000,
  "5": 9999999
};
// 消息数据的响应式引用
const messages = ref([]);
// 组件挂载后请求用户数据
onMounted(() => {
  fetchUserData();
  fetchMessages(); // 获取消息数据
});

// 获取用户数据的函数
async function fetchUserData() {
  try {
    // TODO url 修改后端请求地址 获取用户消息
    const response = await axios.get('http://127.0.0.1:8000/get_user/',{params:{username:sessionStorage.getItem("username")}});
    if (response.data["status"] === "ok" ) {
      user.value = response.data["data"];
      user.value.userBalance = Number(user.value.userBalance.toFixed(2))
      upEXP.value = dictionary[user.value.userCreditRank]
    } else if (response.data["status"] === "error" ) {
      ElMessage.error('请求用户数据失败');
    }
  } catch (error) {
    console.error('请求用户数据失败：', error);
    ElMessage.error('请求用户数据失败');
  }
}
// 获取消息数据的函数
async function fetchMessages() {
  try {
    const params = { username: sessionStorage.getItem("username") };
    // TODO url 修改后端请求地址
    const response = await axios.get('http://127.0.0.1:8000/get_messages/', { params });
    if (response.data.status === "ok") {
      messages.value = response.data.data;
      console.log(messages.value)
    } else {
      ElMessage.info('没有消息');
    }
  } catch (error) {
    console.error('获取消息失败：', error);
    ElMessage.error('获取消息失败');
  }
}

const rechargeAmount = ref('');
const handleRecharge = async () => {
  // 检查充值金额是否有效
  if (!rechargeAmount.value.trim()) {
    ElMessage.error('请输入充值金额');
    return;
  }
  const amount = parseFloat(rechargeAmount.value);
  if (isNaN(amount) || amount <= 0) {
    ElMessage.error('充值金额必须是正数');
    return;
  }

  try {
    // TODO url 修改请求地址
    const response = await axios.get('http://127.0.0.1:8000/top_up/', {params:{username: user.value.username,balance_change: amount}});
    // 处理响应
    if (response.data.status === "ok") {
      console.log('充值成功', response.data);
      ElMessage.success('充值成功');
      user.value.userBalance += amount;
      rechargeAmount.value='';
    } else if (response.data.status === "error")  {
      ElMessage.error('充值失败');
    }
  } catch (error) {
    console.log(error)
    ElMessage.error('error');
  }
};

// 提交表单的函数
function submitForm() {
  // 在这里添加更新用户数据的逻辑
  // 通常需要调用 API 更新服务器上的数据
  console.log('提交表单的逻辑');
  // 假设更新成功
  ElMessage.success('个人信息更新成功');
}


</script>

<style scoped lang="scss">
.layout-container {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.el-header {
  padding: 20px;
}
</style>