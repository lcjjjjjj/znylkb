<script setup lang="ts">
import { ElMessageBox } from 'element-plus';
import { postText } from '@/api';
import { ref, computed } from 'vue'
import { useStore } from 'vuex';
import type { TabsPaneContext } from 'element-plus';
const textarea = ref('')
const result = ref('')

const onClick = () => {
    postText({text: textarea.value}).then((res) => {
        console.log(res)
        result.value = res.data.msg
    })
}

const saveFile = () => {
    if (result.value !== ''){
        const fileContent = result.value
        const blob = new Blob([fileContent],{ type: 'text/plain' })
        const link = document.createElement('a')
        const url = window.URL.createObjectURL(blob)
        link.href = url
        link.download = 'save.txt'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
    }
    else{
        ElMessageBox.alert('保存的内容不能为空','温馨提示',{confirmButtonText: '确定',})
    }
}

const activeName = ref('first')

const handleClicktab = (tab: TabsPaneContext, event: Event) => {
  console.log(tab.props.name, event)
}

const selectStyle = (item:any)=>{
  if(item.role === 'user'){
    return 'scrollbar-user'
  }
  else{
    return 'scrollbar-assistant'
  }
}

const store = useStore()
const input_text = ref('')
// const messageCache = []
const messageItem = computed(() => store.state.message.sendMessage).value

const sendMessage = () => {
  store.commit('addMsg',{'role': 'user','msg': input_text.value})
  // console.log(messageCache)
  input_text.value = ''
}




</script>

<template>
  <div class="work-area">
    <el-tabs tab-position="left" v-model="activeName" class="demo-tabs" @tab-click="handleClicktab">
      <el-tab-pane label="文本转写" name="first" class="convert-text">
        <div class="textsum-area">
            <el-input
                v-model="textarea"
                :rows="13"
                type="textarea"
                placeholder="请输入文本"
            />
        </div>
        <div class="buttons">
            <el-button type="primary" round @Click="onClick">改写</el-button>
            <el-button type="success" round @Click="saveFile">保存</el-button>
        </div>
        <div class="textsum-area">
            <el-input
                v-model="result"
                :rows="13"
                type="textarea"
                placeholder="改写结果"
            />
        </div>
      </el-tab-pane>
      <el-tab-pane label="文本翻译" name="second" class="translate-text">
        <el-scrollbar height="600px">
          <div v-for="item in messageItem" :key="item" :class="selectStyle(item)">
            <p v-if="item.role === 'user'">用户</p>
            <p v-if="item.role === 'assistant'">智能助手</p>
            <div class="dialog">
              {{ item.msg }}
            </div>
          </div>
        </el-scrollbar>
        <div class="translate-input-area">
          <el-input
                v-model="input_text"
                :rows="6"
                type="textarea"
                placeholder="请输入文本"
          />
        </div>
        <div class="button-area">
          <el-button type="success" circle size="large" @click="sendMessage">
            <el-icon><Check /></el-icon>
          </el-button>
          <el-button type="danger" circle size="large">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
      </el-tab-pane>
      <el-tab-pane label="文本摘要" name="third">文本摘要</el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.work-area {
    padding-top: 100px;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 900px;
}

.convert-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 800px;
}

.translate-text {
  /* background-color: deeppink; */
  border: 1px solid #c6ced5;
  border-radius: 4px;
  width: 800px;
}

.textsum-area {
  display: flex;
  justify-content: center;
  padding: 0px 10px;
  position: relative;
  text-align: center;
  width: 100%;
}

.buttons {
  display: flex;
  justify-content: center;
  position: relative;
  padding: 15px;
  width: 100%;
}


.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

/* 修改内部定义的颜色 */
.el-tabs :deep(.el-tabs__item.is-active) {
  color: #ffd04b;
}

.el-tabs :deep(.el-tabs__item:hover) {
  color: #ffd04b;
}

.el-tabs :deep(.el-tabs__active-bar){
  background-color: #ffd04b;
}

/* .scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
} */

.scrollbar-assistant {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: 10px;
  align-items: flex-start;
  border-radius: 4px;
}

.scrollbar-user {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: 10px;
  align-items: flex-end;
  border-radius: 4px;
}

.dialog {
  max-width: 500px;
  background-color: #ffd04b;
  border-radius: 4px;
  margin-top: 5px;
  padding: 10px;
}

.translate-input-area {
  margin: 10px;
}

.button-area {
  display: flex;
  padding: 0px 10px 10px 0px;
  justify-content: flex-end;
}
</style>