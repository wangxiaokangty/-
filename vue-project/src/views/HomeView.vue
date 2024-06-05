<template>
  <!--  element-plus的容器-->
  <el-container class="layout-container">
    <!-- 左侧菜单 -->
    <NavBar/>
    <!-- 右侧主区域 -->
    <el-container>
      <!-- 头部区域 -->
      <el-header v-if="loginFlag">
        <div style="text-align: center;"><strong>{{ username }}，欢迎来到本数据标注平台！</strong></div>
        <!--下拉菜单-->
        <el-dropdown @command="handleCommand" placement="bottom-end">
          <span class="el-dropdown__box">
            <el-avatar :src="avatar" />
            <el-icon>
              <CaretBottom />
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout" :icon="SwitchButton">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-header v-else>
        <div ><strong>欢迎来到本数据标注平台！</strong>
          <el-button type="primary" @click="goToLogin">登录</el-button></div>
      </el-header>
      <!-- 中间区域 -->
      <el-main>
        <div style="width: 1290px; height: 570px; border: 1px solid red;">
          内容展示区
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  SwitchButton,
  CaretBottom
} from '@element-plus/icons-vue'
import avatar from '@/assets/default.png'
import NavBar from '@/components/NavBar.vue' // 导入NavBar组件


const username = ref('')
const router = useRouter()
const loginFlag = ref(false)


//onMounted(() => {
//  username.value = localStorage.getItem('username') || '未登录用户'
//  loginFlag.value = localStorage.getItem('logined') === 'true'
//})
onMounted(() => {
  username.value = sessionStorage.getItem('username') || '未登录用户'
  loginFlag.value = sessionStorage.getItem('logined') === 'true'
})
const handleCommand = (command) => {
  if (command === 'logout') {
    sessionStorage.removeItem('logined')
    sessionStorage.removeItem('username')
    //localStorage.removeItem('login_jwt')
    router.push('/login')
  } else {
    // Handle other commands if necessary
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>


<style lang="scss" scoped>
.layout-container {
  height: 100vh;

  .el-aside {
    background-color: #232323;

    &__logo {
      height: 120px;
      background: url('@/assets/logo.png') no-repeat center / 120px auto;
    }

    .el-menu {
      border-right: none;
    }
  }

  .el-header {
    background-color: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;

    .el-dropdown__box {
      display: flex;
      align-items: center;

      .el-icon {
        color: #999;
        margin-left: 10px;
      }

      &:active,
      &:focus {
        outline: none;
      }
    }
  }

  .el-footer {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: #666;
  }
}
</style>
