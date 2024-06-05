<template>
  <el-aside width="200px">
    <div class="el-aside__logo"></div>
    <el-menu
        router
        :default-active="activeIndex"
        active-text-color="#ffd04b"
        background-color="#232323"
        text-color="#fff"
        @select="handleSelect"
    >
      <!-- 首页 -->
      <el-menu-item index="/home">
        <template #title>
          <span>首页</span>
        </template>
      </el-menu-item>
      <!-- 发布任务界面 -->
      <el-menu-item index="/post-task">
        <template #title>
          <span>发布任务</span>
        </template>
      </el-menu-item>
      <!-- 任务广场 -->
      <el-menu-item index="/task-market">
        <template #title>
          <span>任务广场</span>
        </template>
      </el-menu-item>
      <!-- 个人主页 -->
      <el-sub-menu index="4">
        <template #title>
          <span>个人主页</span>
        </template>
        <el-menu-item index="/personal-info">
          <template #title>
            <span>个人信息</span>
          </template>
        </el-menu-item>
        <el-menu-item index="/posted-tasks">
          <template #title>
            <span>已发布任务</span>
          </template>
        </el-menu-item>
        <el-menu-item index="/tasks-to-complete">
          <template #title>
            <span>已领取任务</span>
          </template>
        </el-menu-item>
      </el-sub-menu>
      <!-- 管理界页 -->
      <el-sub-menu index="5">
        <template #title>
          <span>管理页面</span>
        </template>
        <el-menu-item index="/admin-task">
          <template #title>
            <span>数据审核</span>
          </template>
        </el-menu-item>
        <el-menu-item index="/admin-report">
          <template #title>
            <span>举报处理</span>
          </template>
        </el-menu-item>
      </el-sub-menu>
    </el-menu>
  </el-aside>
</template>

<script setup>
import { ref,onMounted } from 'vue'
import { useRoute} from 'vue-router'
import {
  ElAside,
  ElMenu,
  ElMenuItem,
  ElSubMenu,
} from 'element-plus'
import router from "@/router";

const activeIndex = ref('/') // 默认选中首页
const route = useRoute()
const loginFlag = ref(false)
const adminFlag =ref(false)

onMounted(async () => {
  // 在组件挂载后检查登录状态
  loginFlag.value = sessionStorage.getItem("logined") === 'true';
  activeIndex.value = route.path;
  adminFlag.value = sessionStorage.getItem("adminAuth") === 'true';
});

const handleSelect = (index) => {
   //检查登录状态的逻辑（如果需要）
   if (!loginFlag.value && index !== '/home') {
     alert('请先登录！');
     router.push('/login');
     return;
   }
   if (!adminFlag.value && index.startsWith('/admin')) {
     alert('您不具备管理员权限！！！');
     router.push(route.path);
     return;
   }
  // 更新 activeIndex 的值
  activeIndex.value = index;
  router.push(index);
};


</script>

<style lang="scss" scoped>
.el-aside {
  background-color: #232323;
  height: 100vh;
  overflow: auto;

  &__logo {
    height: 120px;
    background: url('@/assets/logo.png') no-repeat center / 120px auto;
  }

  .el-menu {
    border-right: none;
  }
}
</style>