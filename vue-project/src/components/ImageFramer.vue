<template>
  <div class="parent-container">
    <el-card shadow="never" style="width: 60%">
      <div id="image-label-area"></div>
    </el-card>
  </div>
  <el-card v-if="currentLabel" class="label-info">
    <div class="label-info-content">
      <div class="label-name-input">
        <label for="label-name">标签名称:</label>
        <el-input id="label-name" type="text" v-model="currentLabel.name" @change="updateLabelName"
                  style="width: 240px" placeholder="请输入对象名称" />
        <label for="label-color">标签颜色:</label>
        <el-color-picker id="label-color" type="color" v-model="currentLabel.color" @change="updateLabelColor" />
      </div>
      <label>(x: {{ currentLabel.x }}, y: {{ currentLabel.y }})</label>
      <label>宽度: {{ currentLabel.width}}  高度: {{ currentLabel.height}}</label>
      <el-button type="danger" @click="removeLabel(currentLabel.uuid)">删除</el-button>
    </div>
    <div class="button-group">
      <el-button type="primary" @click="removeAllLabels" >一键删除</el-button>
      <el-button type="primary" @click="saveLabels">保存标签结果</el-button>
    </div>
  </el-card>
  <el-card v-else>
    <p>共标注 {{labelsCount}} 条数据</p>
    <div class="button-group">
      <el-button type="primary" @click="removeAllLabels" >一键删除</el-button>
      <el-button type="primary" @click="saveLabels">保存标签结果</el-button>
    </div>
  </el-card>
</template>
<script setup>

import {ref, defineProps,defineEmits, watch, onMounted} from 'vue';
import SimpleImageLabel from 'simple-image-label';
const simpleImageLabel = ref(null);
const currentLabel = ref(null);
let labelsCount =ref(0)
const props = defineProps({
  subtask:Object
});
const emit = defineEmits(['contextmenu', 'labelClick', 'error', 'labelRemoved', 'labelUpdated','saveLabelsToAnswer']);

onMounted(() => {
  if (!props.subtask.content) {
    console.error('Image URL is required');
    return;
  }

  simpleImageLabel.value = new SimpleImageLabel({
    el: 'image-label-area',
    imageUrl: props.subtask.content,
    labels: [],
    contextmenu: (e) => {
      emit('contextmenu', e);
    },
    labelClick: (label) => {
      currentLabel.value = label;
      emit('labelClick', label);
      labelsCount.value = simpleImageLabel.value.labels.length;
    },
    error: (e) => {
      emit('error', e);
    }
  });
});
watch(() => props.subtask, () => {
  // 当 subtask 发生变化时，执行以下操作
  simpleImageLabel.value.setImage(props.subtask.content);
  simpleImageLabel.value.setLabels([]);
  currentLabel.value = null;
  labelsCount.value =0;
});
const saveLabels = () => {
  const annotationData = simpleImageLabel.value.getLabels();
//  let processedData = annotationData.map(label => {
//    return {
//      name: label.name,
//      yolo:{x: label.x,
//        y: label.y,
//        width: label.width,
//        height: label.height},
//      coordinate: simpleImageLabel.value.getCoordinate(label)
//    };
//  });
  emit("saveLabelsToAnswer",JSON.stringify(annotationData));
}
const removeAllLabels = () => {
  simpleImageLabel.value.removeAllLabels();
  labelsCount.value =0;
  currentLabel.value = null;
};
const removeLabel = (uuid) => {
  simpleImageLabel.value.removeLabelByUuid(uuid);
  currentLabel.value = null;
  emit('labelRemoved', uuid);
};

const updateLabelName = () => {
  simpleImageLabel.value.setLabelByUuid(currentLabel.value.uuid, {
    name: currentLabel.value.name
  });
  emit('labelUpdated', currentLabel.value);
};

const updateLabelColor = () => {
  simpleImageLabel.value.setLabelByUuid(currentLabel.value.uuid, {
    color: currentLabel.value.color
  });
  emit('labelUpdated', currentLabel.value);
};
</script>

<style scoped>
.parent-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}
.button-group {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
.label-info {
  margin-top: 20px;
}


.label-info-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.label-name-input,
.label-color-input {
  display: flex;
  align-items: center;
}

.label-name-input label,
.label-color-input label {
  width: 80px;
}

.label-name-input input,
.label-color-input input {
  flex: 1;
}
</style>