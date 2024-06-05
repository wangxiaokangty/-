<template>
  <el-container class="layout-container">
    <!-- 左侧菜单 -->
    <NavBar/>
    <el-container>
      <el-header style="font-size: large; display: flex; justify-content: center; align-items: center;">
        任务发布界面
      </el-header>
      <!-- 个人信息 -->
      <el-card header="个人信息" shadow="never">
        <UserInformation current-page="post-task"/>
      </el-card>
      <!-- 发布任务 -->
      <el-card header="发布任务设置" shadow="never">
        <el-form :model="form" label-width="auto" style="max-width: 80%  ;margin: 0 auto">
          <el-form-item label="任务名称">
            <el-input v-model="form.task_name" placeholder="输入任务名称" />
          </el-form-item>
            <el-form-item label="数据类型">
              <el-select v-model="form.data_type" style="max-width: 25%">
                <el-option label="文本类型" value="文本" />
                <el-option label="图像类型" value="图片" />
              </el-select>
            </el-form-item>
          <div style="display: inline-block; width: 30%;">
            <el-form-item label="任务星级">
              <el-rate v-model="form.task_rank" :texts="[1, 2, 3, 4, 5]" show-text />
            </el-form-item>
          </div>
          <div style="display: inline-block; width: 35%;">
            <el-form-item label="标注报酬">
              <el-input-number v-model="form.each_pay" :precision="2" :step="0.05" :min="0" size="small" />
              <span>&nbsp;&nbsp;元/条数据</span>
            </el-form-item>
          </div>
          <el-form-item label="任务描述">
            <el-input v-model="form.task_description" type="textarea"/>
          </el-form-item>
          <el-form-item label="问题题干">
            <el-input v-model="form.question_description" type="textarea"/>
          </el-form-item>
          <el-form-item label="问题类型">
            <el-select v-model="form.question_type">
              <el-option label="单选题" value="单选题" />
              <el-option label="多选题" value="多选题" />
              <el-option label="填空题" value="填空题" />
              <el-option v-if="form.data_type ==='图片'"  label="框图题" value="框图题" />
            </el-select>
          </el-form-item>
          <el-card v-if="form.question_type === '单选题'|| form.question_type === '多选题'" shadow="never">
            <!-- 添加选项的表单项 -->
            <el-form-item label="选项">
              <!-- 使用 Flex 布局 -->
              <div style="display: flex; align-items: center;">
                <!-- 选项内容输入框 -->
                <el-input v-model="optionText" placeholder="请输入选项内容" style="flex: 1;" />
                <!-- 添加选项按钮 -->
                <el-button @click="addOption" type="primary">添加选项</el-button>
              </div>
            </el-form-item>
            <div v-if="form.options.length">
              <ul>
                <li v-for="(option, index) in form.options" :key="index">
                  {{ option }}
                  <!-- 删除选项按钮 -->
                  <el-button type="text" @click="removeOption(index)">删除</el-button>
                </li>
              </ul>
            </div>
          </el-card>
          <el-form-item label="截止时间">
            <el-col :span="11">
              <el-date-picker v-model="form.deadline_time" type="date" placeholder="Pick a date" style="width: 100%" :disabledDate="disabledDate" />
            </el-col>
          </el-form-item>

          <!-- 文件上传组件 -->
          <el-form-item label="上传文件" v-if="form.data_type === '文本'" class="file-upload-item">
            <el-button type="primary" @click="chooseFile('text')">选择CSV文件</el-button>
            <input type="file" id="fileInputText" @change="handleFileChange" accept=".csv" style="display: none;"/>
            <div v-if="fileName" class="file-name">&nbsp;已选择文件: {{ fileName }}</div>
            <div v-else class="file-prompt">&nbsp;请选择一个CSV文件</div>
            <el-link v-if="fileName" class="file-prompt" type="danger" @click="removeFile('fileInputText')">&nbsp;删除</el-link>
          </el-form-item>

          <el-form-item label="上传文件" v-else-if="form.data_type === '图片'" class="file-upload-item">
            <el-button type="primary" @click="chooseFile('image')">选择ZIP文件</el-button>
            <input type="file" id="fileInputImage" @change="handleFileChange" accept=".zip" style="display: none;"/>
            <div v-if="fileName" class="file-name">&nbsp;已选择文件: {{ fileName }}</div>
            <div v-else class="file-prompt">&nbsp;请选择一个仅包含图片的ZIP文件</div>
            <el-link v-if="fileName" class="file-prompt" type="danger" @click="removeFile('fileInputText')">&nbsp;删除</el-link>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="onSubmit">创建任务</el-button>
            <el-button @click="clickHome">取消创建</el-button>
          </el-form-item>
        </el-form>
    </el-card>
    </el-container>
  </el-container>
</template>

<script setup>
import NavBar from "@/components/NavBar.vue";
import UserInformation from "@/components/UserInformation.vue";
import {ref,onMounted} from "vue";
import router from "@/router";
import axios from "axios";
import {ElMessageBox} from "element-plus";

// Define your data model
const form=ref({
  task_name: '',
  task_description: '',
  data_type: '文本',
  task_rank: 1,
  each_pay: 0.05,
  question_description:'',
  question_type: '填空题',
  options: [],
  publisher: '',
  deadline_time: null, // For date picker
})
const fileName = ref('');
onMounted(()=>{
})

// Option text state for adding new options
const optionText = ref('');
// Methods to handle form interactions
const addOption = () => {
  if (optionText.value.trim()) {
    form.value.options.push(optionText.value);
    optionText.value = ''; // Reset input after adding
  }
};
const removeOption = (index) => {
  form.value.options.splice(index, 1);
};

// Placeholder onSubmit function, replace with actual logic
const onSubmit = async () => {
  // 表单验证逻辑（示例）
  if (!form.value.task_name) {
    alert('请填写任务名称。');
    return;
  } else if (!form.value.task_description) {
    alert('请填写任务描述。');
    return;
  } else if (!form.value.question_description) {
    alert('请填写问题题干。');
    return;
  } else if (!form.value.deadline_time) {
    alert('请选择截止日期');
    return;
  }

  if (form.value.data_type === '文本' && !fileName.value) {
    alert('请上传CSV文件。');
    return;
  }

  if (form.value.data_type === '图片' && !fileName.value) {
    alert('请上传ZIP文件。');
    return;
  }

  try {
    // 构建FormData对象
    let formData = new FormData();
    formData.append('task_name', form.value.task_name);
    formData.append('data_type', form.value.data_type);
    formData.append('task_rank', form.value.task_rank);
    formData.append('each_pay', form.value.each_pay);
    formData.append('task_description', form.value.task_description);
    formData.append('question_description', form.value.question_description);
    formData.append('question_type', form.value.question_type);
    formData.append('options',JSON.stringify(form.value.options))
    formData.append('deadline_time', form.value.deadline_time.toISOString());
    formData.append('publisher', sessionStorage.getItem("username"));
    // 如果有文件上传，添加文件到FormData
    if (form.value.data_type === '文本' && document.getElementById('fileInputText').files[0]) {
      formData.append('file', document.getElementById('fileInputText').files[0], fileName.value);
    } else if (form.value.data_type === '图片' && document.getElementById('fileInputImage').files[0]) {
      formData.append('file', document.getElementById('fileInputImage').files[0], fileName.value);
    }
    // // TODO url 请求地址修改 发送POST请求到服务器
    const response = await axios.post('http://127.0.0.1:8000/post_task/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // 重要：设置正确的Content-Type
      },
    });

    // 处理响应
    const responseData = response.data;
    if (responseData.status === 'ok') {
      // 使用ElMessageBox.confirm来弹出成功确认对话框
      ElMessageBox.confirm(responseData.message, '成功', {
        confirmButtonText: '确定',
        type: 'success',
      }).then(() => {
        // 用户点击“确定”后的操作，例如导航到首页
        router.push('/posted-tasks');
      }).catch(() => {
        // 用户点击取消或关闭对话框
        router.push('/posted-tasks');
      });
    } else {
      // 使用ElMessageBox.alert来弹出错误消息框
      ElMessageBox.alert(responseData.message, '操作失败', {
        confirmButtonText: '确定',
        type: 'error',
      }).catch(() => {});
    }
  } catch (error) {
    // 错误处理
    ElMessageBox.alert('任务创建失败，请稍后重试。', '错误', {
      confirmButtonText: '确定',
      type: 'error',
    }).catch(() => {});
    console.error('任务创建失败：000000', error);
  }
};

// Navigate back to home
const clickHome = () => {
  // Implement navigation logic here, e.g., router.push('/')
  router.push('/home')
  console.log('Navigating back home');
};


const chooseFile = (type) => {
  // 根据类型选择文件输入
  const fileInputId = type === 'text' ? 'fileInputText' : 'fileInputImage';
  document.getElementById(fileInputId).click();
};
const handleFileChange = (e) => {
  if (e.target.files === null || e.target.files.length === 0) {
    return;
  }

  const file = e.target.files[0];
  const validExtensions = form.value.data_type === '文本' ? ['.csv'] : ['.zip'];
  const fileExtension = '.'+file.name.split('.').pop();

  if (validExtensions.includes(fileExtension)) {
    fileName.value = file.name;
  } else {
    alert(`请上传${form.value.data_type === '文本' ? 'CSV' : 'ZIP'}文件.`);
    fileName.value = '';
  }
};
// 处理删除文件的方法
const removeFile = (fileInputId) => {
  // 清空对应的文件输入字段
  const fileInput = document.getElementById(fileInputId);
  fileInput.value = '';
  // 重置fileName和fileSize
  fileName.value = '';
};

// 计算属性或方法，用于禁用当前日期和之前的日期
const disabledDate = (date) => {
  const today = new Date();
  // 设置时间为0时，即当天的开始时间（00:00:00），确保整天都是禁用的
  today.setHours(0, 0, 0, 0);
  return date && date <= today;
};
</script>

<style scoped>
.file-upload-item {
  margin-bottom: 20px; /* 为组件添加一些间隔 */
}

.file-name {
  margin-top: 8px; /* 与按钮保持间隔 */
  color: #409eff; /* 例如，Element UI的主要颜色 */
  font-size: 14px;
}

.file-prompt {
  margin-top: 8px;
  color: #909399; /* 灰色提示文本 */
  font-size: 12px;
}
</style>
