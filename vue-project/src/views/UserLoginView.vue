<template>
  <el-row class="login-page">
    <el-col :span="12" class="bg"></el-col>
    <el-col :span="6" :offset="3" class="form">
      <!-- 注册表单 -->
      <el-form ref="form" size="large" autocomplete="off" v-if="isRegister" :model="registerData" :rules="rules">
        <el-form-item>
          <h1>注册</h1>
        </el-form-item>
        <el-form-item prop="username">
          <el-input :prefix-icon="User" placeholder="请输入用户名" v-model="registerData.username"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input :prefix-icon="Lock" type="password" placeholder="请输入密码" v-model="registerData.password"></el-input>
        </el-form-item>
        <el-form-item prop="rePassword">
          <el-input :prefix-icon="Lock" type="password" placeholder="请再次输入密码" v-model="registerData.rePassword"></el-input>
        </el-form-item>
        <el-form-item prop="email">
          <el-input :prefix-icon="Message" placeholder="请输入邮箱" v-model="registerData.email"></el-input>
        </el-form-item>
        <el-form-item prop="verifyCode">
          <el-col :span="14">
          <el-input :prefix-icon="Lock" placeholder="请输入验证码" v-model="registerData.verifyCode"></el-input>
          </el-col>
          <el-col :span="10">
            <el-button class="get-verify" @click="getVerifyCode">获取验证码</el-button>
          </el-col>
        </el-form-item>
        <!-- 注册按钮 -->
        <el-form-item>
          <el-button class="button" type="primary" auto-insert-space @click="clickRegister">
            注册
          </el-button>
        </el-form-item>
        <el-form-item class="flex">
          <el-link type="info" :underline="false" @click="isRegister = false">
            ← 返回
          </el-link>
        </el-form-item>
      </el-form>
      <!-- 忘记密码表单 -->
      <el-form ref="forgetPasswordForm" size="large" autocomplete="off" v-if="isRestPwd">
        <el-form-item>
          <h1>重置密码</h1>
        </el-form-item>
        <el-form-item>
          <el-input :prefix-icon="User" placeholder="请输入用户名" v-model="forgetUsername"></el-input>
        </el-form-item>
        <el-form-item prop="email">
          <el-input :prefix-icon="Message" placeholder="请输入您的邮箱" v-model="forgetEmail"></el-input>
        </el-form-item>
        <el-form-item prop="verifyCode">
          <el-col :span="16">
            <el-input :prefix-icon="Lock" placeholder="请输入验证码" v-model="forgetVerifyCode"></el-input>
          </el-col>
          <el-col :span="8">
            <el-button @click="sendVerifyCode">获取验证码</el-button>
          </el-col>
        </el-form-item>
        <el-form-item>
          <el-input placeholder="请输入新密码" v-model="newPassword" type="password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="resetPassword">重置密码</el-button>
        </el-form-item>
        <el-form-item class="flex">
          <el-link type="info" :underline="false" @click="isRestPwd = false">
            ← 返回
          </el-link>
        </el-form-item>
      </el-form>


      <!-- 登录表单 -->
      <el-form ref="form" :model="loginData" size="large" autocomplete="off" v-if="!isRestPwd && !isRegister">
        <el-form-item>
          <h1>登录</h1>
        </el-form-item>
        <el-form-item>
          <el-input :prefix-icon="User" placeholder="请输入用户名" v-model="loginData.username"></el-input>
        </el-form-item>
        <el-form-item>
          <el-input name="password" :prefix-icon="Lock" type="password" placeholder="请输入密码" v-model="loginData.password"></el-input>
        </el-form-item>
        <el-form-item class="flex">
          <div class="flex">
            <el-link type="primary" :underline="false" @click="isRestPwd = true">忘记密码？</el-link>
          </div>
        </el-form-item>
        <!-- 登录按钮 -->
        <el-form-item>
          <el-button class="button" type="primary" auto-insert-space @click="clickLogin">登录</el-button>
        </el-form-item>
        <el-form-item class="flex">
          <el-link type="info" :underline="false" @click="isRegister = true">
            注册 →
          </el-link>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<script setup>
import { User, Lock, Message } from '@element-plus/icons-vue'
import { ref } from 'vue'
import axios from "axios";
import {ElMessage} from "element-plus";
import {useRouter} from "vue-router";
//控制注册与登录表单的显示， 默认显示注册
const isRegister = ref(false);
const isRestPwd = ref(false);
const correctCode = ref("");
const emailRight = ref(false);
const emailing = ref(false);
const codeEmail = ref("");
const emailingSeconds = ref(0);
const usernameRight = ref(false);
const passwordRight = ref(false);
const passwordAgainRight = ref(false);
const verifyCodeRight = ref(false);
const { push } = useRouter();
// 定义数据模型
//登录
const loginData = ref({
  username: "",
  password: "",
})


const clickLogin = () => {
  axios
      // TODO url 请求地址修改
      .get("http://127.0.0.1:8000/log_in/", {
        params: {
          username: loginData.value.username,
          password: loginData.value.password,
        },
      })
      .then((res) => {
        console.log(res.data)
        if (res.data["status"] === "error") {
          if (res.data["message"] === "noUser") {
            ElMessage({
              type: "error",
              message: "用户不存在或用户名错误",
            });
          } else if (res.data["message"] === "wrongPassword") {
            ElMessage({
              type: "error",
              message: "密码错误",
            });
          } else {
            ElMessage({
              type: "error",
              message: "登录失败，请稍后再试",
            });
          }
        } else if (res.data["status"] === "ok") {
          ElMessage({
            type: "success",
            message: "登录成功",
          });
          if (res.data["type"] === "admin") {
            sessionStorage.setItem("adminAuth", "true");
          } else if (res.data["type"] === "normal")  {
            sessionStorage.setItem("adminAuth", "false");
          }
          sessionStorage.setItem("logined", "true");
          sessionStorage.setItem("username", loginData.value.username);
          push({
            name: "home"
          });
        }
      })
      .catch(function (err) {
        console.log(err);
      });
};

//注册
const registerData = ref({
  username: '',
  password: '',
  rePassword: '',
  email: '',
  verifyCode: ''
})

const validateUsername = (rule, value, callback) => {
  if (value === "") {
    usernameRight.value = false;
    callback(new Error("用户名不能为空"));
  } else if (value.match(/[a-zA-z\d]{5,12}/g)) {
    usernameRight.value = true;
    callback();
  } else {
    usernameRight.value = false;
    callback(new Error("请输入5-12位字母和数字的组合"));
  }
};


// 校验密码的函数
const validatePassword = (rule, value, callback) => {
  if (value === "") {
    passwordRight.value = false;
    callback(new Error("密码不能为空"));
  } else if (value.search(/^[a-zA-Z\d]{6,18}$/g) === -1) {
    passwordRight.value  = false;
    callback(new Error("请输入6-18位字母和数字的组合"));
  } else {
    passwordRight.value  = true;
    callback();
  }
};
const checkRePassword = (rule, value, callback) => {
  if (value === '') {
    passwordAgainRight.value = false
    callback(new Error('请再次确认密码'))
  } else if (value !== registerData.value.password) {
    passwordAgainRight.value = false
    callback(new Error("请确保两次输入密码一致"))
  } else {
    passwordAgainRight.value = true
    callback()
  }
}

// 校验邮箱格式的函数
const validateEmail = (rule, value, callback) => {
  if (value.match(/[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+/g)) {
    emailRight.value = true;
    callback();
  } else {
    emailRight.value = false;    
    callback(new Error("邮箱格式不合法"));
  }
};


// 校验验证码的函数
const validateVerifyCode = (rule, value, callback) => {
  if (!Number.isInteger(Number(value)) || value.length !== 6) {
    verifyCodeRight.value = false;
    callback(new Error("请输入六位数字验证码"));
  } else {
    verifyCodeRight.value = true;
    callback();
  }
};

// 定义表单校验规则
const rules={
  username:[
    {validator: validateUsername,required:true, message:'请输入用户名', trigger:'blur'},
    {min: 5, max: 16, message: '长度5-16位非空字符', trigger: 'blur'}
  ],
  password:[
    {validator: validatePassword,required:true, message:'请输入密码', trigger:'blur'},
    {min: 5, max: 16, message: '长度5-16位非空字符', trigger: 'blur'}
  ],
  rePassword:[
    { validator: checkRePassword, trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { validator: validateEmail, trigger: 'blur' }
  ],
  verifyCode: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { validator: validateVerifyCode, trigger: 'blur' }
  ]
};

const getVerifyCode = (emailRight) => {
  if (emailRight.value) {
    ElMessage({
      type: "error",
      message: "邮箱格式错误，请进行修改",
    });
    return;
  }
  if (emailing.value) {
    ElMessage({
      type: "warning",
      message: `验证码已发送，${60 - emailingSeconds.value}s后可以重新发送`,
    });
    return;
  }
  codeEmail.value = registerData.value.email;
  emailing.value = true;
  emailingSeconds.value = 0;
  let timerI = setInterval(() => {
    emailingSeconds.value += 1;
  }, 1000);
  let timerT = setTimeout(() => {
    emailing.value = false;
    clearTimeout(timerT);
    clearInterval(timerI);
  }, 60000);
  axios
      // TODO url 请求地址修改
      .get("http://127.0.0.1:8000/log_up/", {
        params: {
          type: "getVerifyCode",
          email: codeEmail.value,
        },
      })
      .then((res) => {
        console.log(res)
        if (res.data["status"] === "ok") {
          correctCode.value = res.data["verifyCode"];
          ElMessage({
            type: "success",
            message: "验证码发送成功，请在对应邮箱查收",
          });
        } else if (res.data["status"] === "wrong") {
          if (res.data["message"] === "sameEmail") {
            ElMessage({
              type: "error",
              message: "该邮箱已被注册",
            });
            emailing.value = false;
            emailingSeconds.value = 0;
            clearTimeout(timerT);
            clearInterval(timerI);
          }
        }
      })
      .catch(function (err) {
        console.log(err);
      });
}

const clickRegister= () => {
  if (
      !(
          usernameRight.value &&
          passwordRight &&
          passwordAgainRight.value &&
          emailRight.value &&
          verifyCodeRight.value
      )
  ) {
    ElMessage({
      type: "error",
      message: "填写信息格式错误，请进行修改",
    });
    return;
  }
  if (registerData.value.email !== codeEmail.value) {
    ElMessage({
      type: "warning",
      message: "填写邮箱与发送验证码时对应邮箱不匹配",
    });
    return;
  }
  if (registerData.value.verifyCode !== correctCode.value) {
    ElMessage({
      type: "error",
      message: "验证码错误",
    });
    return;
  }
  axios
      // // TODO url 请求地址修改
      .get("http://127.0.0.1:8000/log_up/", {
        params: {
          type: "logUp",
          username: registerData.value.username,
          password: registerData.value.password,
          email: registerData.value.email,
          verifyCode: registerData.value.verifyCode,
        },
      })
      .then((res) => {
        console.log(registerData)
        if (res.data["status"] === "ok") {
          ElMessage({
            type: "success",
            message: "注册成功，请返回登录界面",
          });
        } else {
          console.log(res);
          if (res.data["message"] === "sameName") {
            ElMessage({
              type: "error",
              message: "该用户名已注册，请选择其他用户名",
            });
          } else if (res.data["message"] === "unknown") {
            ElMessage({
              type: "error",
              message: "注册失败，未知错误",
            });
          }
        }
      })
      .catch(function (err) {
        console.log(err);
      });
}


// 前端脚本
const forgetUsername = ref('');
const forgetEmail = ref('');
const forgetVerifyCode = ref("");
const forgetVerifyCode2 = ref("");
const newPassword = ref('');
const sendVerifyCode = () => {
  if (!forgetUsername.value){
    ElMessage.error('用户名不能为空');
    return;
  }
  // 验证邮箱格式
  if (!forgetEmail.value.match(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/)) {
    ElMessage.error('邮箱格式不正确');
    return;
  }

  // TODO url 发送验证码请求
  axios.get('http://127.0.0.1:8000/send-verify-code/', {
    params: {
      username:forgetUsername.value,
      email: forgetEmail.value,
    },
  }).then((res) => {
    if (res.data.status === "ok") {
      ElMessage.success('验证码已发送至您的邮箱');
      forgetVerifyCode2.value = res.data["verifyCode"];
    } else if (res.data.status === "error"){
      ElMessage.error(res.data.message);
    }
  }).catch(error => {
    console.error('发送验证码失败:', error);
    ElMessage.error('发送验证码失败，请稍后重试',error);
  });
};


const resetPassword = () => {
  // 验证验证码和新密码
  if (!forgetVerifyCode.value || !newPassword.value) {
    ElMessage.error('请填写验证码和新密码');
    return;
  }
  if (forgetVerifyCode.value !== forgetVerifyCode2.value) {
    ElMessage.error('验证码错误，请仔细阅读邮件最新验证码');
    return;
  }
  const data ={
    username:forgetUsername.value,
    email: forgetEmail.value,
    newPassword: newPassword.value,
  }
  const header = {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  }
  // TODO url 提交新密码
  axios.post('http://127.0.0.1:8000/reset_password/', data ,header).then((res) => {
    if (res.data.status === "ok") {
      ElMessage.success('密码重置成功');
      isRestPwd.value=false
      forgetVerifyCode.value = "";
      forgetVerifyCode2.value = "";
      newPassword.value = '';
    }
  }).catch(error => {
    console.error('密码重置失败:', error);
    ElMessage.error('密码重置失败，请稍后重试');
  });
};


</script>


<style lang="scss" scoped>
  /* 样式 */
  .login-page {
  height: 100vh;
  background-color: #fff;

  .bg {
  background: url('@/assets/logo2.png') no-repeat 60% center / 240px auto,
  url('@/assets/login_bg.jpg') no-repeat center / cover;
  border-radius: 0 20px 20px 0;
}

  .form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  user-select: none;

  .title {
  margin: 0 auto;
}

  .button {
  width: 100%;
}

  .flex {
  width: 100%;
  display: flex;
  justify-content: space-between;
}
}
}
</style>