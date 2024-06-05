<template>
  <div class="parent-container">
    <el-card shadow="never" style="width: 60%">
      <div id="image-label-area"></div>
    </el-card>
  </div>
</template>
<script setup>

import {ref, defineProps,watch, onMounted} from 'vue';
import SimpleImageLabel from 'simple-image-label';
const simpleImageLabel = ref(null);
const props = defineProps({
  subtask:Object
});
onMounted(() => {
  if (!props.subtask.content) {
    console.error('Image URL is required');
    return;
  }

  simpleImageLabel.value = new SimpleImageLabel({
    el: 'image-label-area',
    imageUrl: props.subtask.content,
    labels: JSON.parse(props.subtask.answer),
    readOnly:true,
  });
});
watch(() => props.subtask, () => {
  // 当 subtask 发生变化时，执行以下操作
  simpleImageLabel.value.setImage(props.subtask.content);
  simpleImageLabel.value.setLabels(JSON.parse(props.subtask.answer));
});
</script>

<style scoped>
.parent-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}
</style>