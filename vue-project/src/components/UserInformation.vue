<template>
  <!-- 不同页面显示不同用户信息，提醒用户 -->
  <el-descriptions size="large" border column=4 v-if="props.currentPage === 'task-market'">
    <el-descriptions-item label="用户名称" width="12.5%">{{user.username}}</el-descriptions-item>
    <el-descriptions-item label="信誉等级" width="12.5%">{{ user.userCreditRank }}</el-descriptions-item>
    <el-descriptions-item label="信誉经验" width="12.5%">{{ user.userCurrentExp}}</el-descriptions-item>
    <el-descriptions-item label="可领取任务星级" width="12.5%">{{ user.userCreditRank}}</el-descriptions-item>
    <el-descriptions-item label="注意:" >
      <span style="color: red">1. 请注意标注质量！发布者反馈任务质量将影响您的信誉经验！</span><br>
      <span style="color: red">2. 请注意任务的截止日期，逾期后未完成将影响您的信誉经验！（不包含发布者提前终止任务情况）</span>
    </el-descriptions-item>
  </el-descriptions>

  <el-descriptions size="large" border column=2 v-if="props.currentPage === 'post-task'">
    <el-descriptions-item label="用户名称" width="12.5%">{{ user.username }}</el-descriptions-item>
    <el-descriptions-item label="当前余额" width="12.5%">{{ user.userBalance }}</el-descriptions-item>
  </el-descriptions>

  <el-descriptions size="large" border column="4" v-if="props.currentPage === 'task-detail'">
    <el-descriptions-item label="用户名称" width="12.5%">{{ user.username }}</el-descriptions-item>
    <el-descriptions-item label="信誉等级" width="12.5%">{{ user.userCreditRank }}</el-descriptions-item>
    <el-descriptions-item label="可领取任务星级" width="12.5%">{{ user.userCreditRank }}</el-descriptions-item>
    <el-descriptions-item label="注意:" >
      <span style="color: red">标注时，请注意标注质量！</span>
    </el-descriptions-item>
  </el-descriptions>


</template>


<script setup>
import axios from "axios";
import { ref, onMounted} from "vue";
// 导入defineProps函数
import { defineProps } from 'vue';
import {ElMessage} from "element-plus";
const props = defineProps({
  currentPage:String,
})

const user = ref({
  user_id:1,
  username: '',
  email: '',
  userBalance: 0,
  userCreditRank: 1,
  userCurrentExp: 0
});
async function fetchUserInfo() {
  try {
    // TODO url 修改请求 合并后端
    // const response = await axios.get('http://127.0.0.1:8000/get_user/',{params:{params:JSON.stringify({username:sessionStorage.getItem("username"),user_id:1})}});
    const response = await axios.get('http://127.0.0.1:8000/get_user/',{params:{username:sessionStorage.getItem("username")}});
    if (response.data["status"] === "ok" ) {
      user.value = response.data["data"];
      console.log()
      user.value.userBalance = Number(user.value.userBalance.toFixed(2))
      sessionStorage.setItem("currentUserBalance",user.value.userBalance.toFixed(2));
    } else if (response.data["status"] === "error" ) {
      ElMessage.error('请求用户数据失败');
    }
  } catch (error) {
    ElMessage.error('请求用户数据失败');
    console.error('获取用户实例失败', error);
  }
}

onMounted(()=>{
  fetchUserInfo();
  sessionStorage.setItem("user",JSON.stringify(user.value));
})
</script>


<style scoped lang="scss">

</style>