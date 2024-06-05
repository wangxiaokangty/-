<template>
  <div>
    <el-card shadow="never">
    <h3>任务描述: </h3>
      <span>{{ currentTask.task_description }}</span>
    <!-- 根据数据类型显示数据内容 -->
      <!-- TODO 加一个问题题干 -->
      <h3>问题题干: </h3>
      <span>{{ currentTask.question_description }}</span>
    <!-- 文本 -->
    <div v-if="currentTask.data_type === '文本'">
      <h3>文本内容: </h3>
      <span>{{ subtask.content }}</span>
        <!-- 假设文本内容存储在 text_content 字段 -->
    </div>
    <!-- 图像 -->
      <el-card shadow="never" v-if="currentTask.data_type === '图片' && currentTask.question_type !== '框图题'">
    <div>
      <el-image :src="subtask.content" alt="任务图片" fit='contain'/> <!-- 假设图片URL存储在 image_url 字段 -->
    </div>
      </el-card>
    </el-card>
    <!-- 根据问题类型显示不同的表单 -->
    <div v-if="currentTask.question_type === '单选题'">
      <el-card shadow="never">
        <el-radio-group v-model="annotationResult">
          <el-radio
              v-for="option in currentTask.options"
              :label="option"
              :key="option"
          >{{ option }}</el-radio>
        </el-radio-group>
      </el-card>

    </div>
    <div v-else-if="currentTask.question_type === '多选题'">
      <el-card shadow="never">
      <el-checkbox-group v-model="annotationResult">
        <el-checkbox
            v-for="option in currentTask.options"
            :label="option"
            :key="option"
        >{{ option }}</el-checkbox>
      </el-checkbox-group>
      </el-card>
    </div>
    <div v-else-if="currentTask.question_type === '填空题'">
      <!-- 无需添加, 在下一个表单编辑并进行提交-->
    </div>
    <div v-else-if="currentTask.question_type === '框图题'">
      <!-- 根据需要添加框图表单 -->
      <ImageFramer :subtask="props.subtask" @save-labels-to-answer="updateAnswer"/>
    </div>

    <!-- 显示标注结果，并提交-->
    <el-card shadow="never">
      <el-form label-width="100px">
        <el-form-item label="标注结果">
          <el-input v-model="annotationResult" placeholder="标注结果" :disabled="currentTask.question_type !== '填空题'" type="textarea" ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitAnnotation">提交标注</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, defineProps, watch } from 'vue';
import axios from 'axios';
import {ElMessage, ElMessageBox} from 'element-plus';
import ImageFramer from "@/components/ImageFramer.vue";
// 定义组件的 props
const props = defineProps({
  currentTask: {
    type: Object,
    required: true
  },
  subtask: {
    type: Object,
    required: true
  }
});

// 创建一个响应式变量来存储标注结果
const annotationResult = ref([]);

// 观察 subtask 变化，以更新 annotationResult
watch(() => props.subtask, () => {
  // 当 subtask 发生变化时，执行以下操作
  annotationResult.value = []; // 重置标注结果
});
const updateAnswer = (Message) =>{
  annotationResult.value = Message;
}
// TODO 提交标注的函数
const submitAnnotation = () => {
  if (!annotationResult.value) {
    ElMessage.error('标注结果不能为空');
    return;
  }

  // 使用 ElMessageBox.confirm 来弹出确认对话框
  ElMessageBox.confirm('提交后无法修改，确定要提交标注结果吗?', '提交确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 用户点击“确定”，发送数据到服务器
    const data = {
      task_id: props.subtask.task,
      subtask_index: props.subtask.subtask_index,
      answer: JSON.stringify(annotationResult.value)
    };
    const header = {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
    }
    // TODO url 修改请求地址
    axios.post(`http://127.0.0.1:8000/submit_subtask_answer/`, data, header)
        // eslint-disable-next-line no-unused-vars
  .then(response => {
      ElMessage.success('标注提交成功');
      // 如果需要，可以在这里添加关闭抽屉的逻辑
      window.location.reload(); // 如果需要刷新页面
    })
        .catch(error => {
          ElMessage.error('标注提交失败');
          console.error('Submit annotation error:', error);
        });
  }).catch(() => {
    // 用户点击“取消”时的逻辑
    ElMessage.info('已取消提交');
  });
};


</script>

<style scoped lang="scss">

</style>