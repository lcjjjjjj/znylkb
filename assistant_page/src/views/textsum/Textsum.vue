<script setup lang="ts">
import Panel from '@/components/Panel.vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { postText } from '@/api';
import { ref,computed,onMounted, onUnmounted } from 'vue'
import { useStore } from 'vuex';
import type { TabsPaneContext, UploadProps } from 'element-plus';
import { UploadInstance } from 'element-plus';
import { isFileServingAllowed } from 'vite';
const textarea = ref('')
const result = ref('')


const activeName = ref('first')
const store = useStore()
const input_text = ref('')
const output_text = ref('')
const uploadRef = ref<UploadInstance>()
// const messageCache = []
let messageItem = computed(() => store.state.message.sendMessage).value
const userItem = computed(() => store.state.user.userInfo).value
console.log(userItem)

const handleClicktab = (tab: TabsPaneContext, event: Event) => {
  console.log(tab.props.name, event)
  store.commit('clearMsg')
  messageItem = computed(()=>store.state.message.sendMessage).value
  if(tab.props.name === 'first'){
    store.commit('addMsg',{'role':'assistant','msg':'请输入文本或文件以进行转换'})
    messageItem = computed(()=>store.state.message.sendMessage).value
  }
  else if(tab.props.name === 'second') {
    store.commit('addMsg',{'role':'assistant','msg':'请输入文本或文件以进行翻译'})
    messageItem = computed(()=>store.state.message.sendMessage).value
  }
  else{
    store.commit('addMsg',{'role':'assistant','msg':'请输入文本或文件以进行摘要'})
    messageItem = computed(()=>store.state.message.sendMessage).value
  }
}

const selectStyle = (item:any)=>{
  if(item.role === 'user'){
    return 'scrollbar-user'
  }
  else{
    return 'scrollbar-assistant'
  }
}

const sendMessage = () => {
  if (input_text.value !== ''){
    store.commit('addMsg',{'role': 'user','msg': input_text.value})
    messageItem = computed(() => store.state.message.sendMessage).value
    // console.log(messageCache)
    postText({text: input_text.value, task: activeName.value}).then((res) => {
        console.log(res)
        output_text.value = res.data.msg
        store.commit('addMsg',{'role': 'assistant','msg': output_text.value})
        messageItem = computed(() => store.state.message.sendMessage).value
    })
    console.log(messageItem)
    input_text.value = ''
  }
  else{
    ElMessageBox.alert('输入的内容不能为空','温馨提示',{confirmButtonText: '确定',})
  }
}

const saveFile = () => {
  messageItem = computed(() => store.state.message.sendMessage).value
  // console.log(messageItem.length)
  if (messageItem.length > 1){
    console.log(messageItem[messageItem.length-1].msg)
    const fileContent = messageItem[messageItem.length-1].msg
    postText({text: fileContent,task: 'save', username: userItem[0]['username']}).then((res) => {
      console.log(res.data.msg)
      if(res.data.msg === 'Done'){
        ElMessage.success('保存成功')
      }
      else{
        ElMessage.error('保存失败')
      }
    })
    // const blob = new Blob([fileContent],{ type: 'text/plain' })
    // const link = document.createElement('a')
    // const url = window.URL.createObjectURL(blob)
    // link.href = url
    // link.download = 'save.txt'
    // document.body.appendChild(link)
    // link.click()
    // document.body.removeChild(link)
    // window.URL.revokeObjectURL(url)
  }
  else{
    ElMessageBox.alert('保存的内容不能为空','温馨提示',{confirmButtonText: '确定',})
  }
}

const clearMessage = () => {
  store.commit('clearMsg')
  messageItem = computed(() => store.state.message.sendMessage).value
  input_text.value = '1'
  input_text.value = ''
  // console.log(activeName.value)
  if(activeName.value === 'first'){
    store.commit('addMsg',{'role':'assistant','msg':'请输入文本或文件以进行转换'})
    messageItem = computed(()=>store.state.message.sendMessage).value
  }
  else if(activeName.value === 'second') {
    store.commit('addMsg',{'role':'assistant','msg':'请输入文本或文件以进行翻译'})
    messageItem = computed(()=>store.state.message.sendMessage).value
  }
  else{
    store.commit('addMsg',{'role':'assistant','msg':'请输入文本或文件以进行摘要'})
    messageItem = computed(()=>store.state.message.sendMessage).value
  }
}

const handleSuccess: UploadProps['onSuccess'] = (file) => {
  console.log(file)
  store.commit('addMsg',{'role': 'user','msg': file.msg})
  messageItem = computed(() => store.state.message.sendMessage).value
  postText({text: file.msg, task: activeName.value}).then((res) => {
    console.log(res)
    output_text.value = res.data.msg
    store.commit('addMsg',{'role': 'assistant','msg': output_text.value})
    messageItem = computed(() => store.state.message.sendMessage).value
  })
  uploadRef.value.clearFiles()
}

onMounted(()=>{
  if(activeName.value === 'first'){
    store.commit('addMsg',{'role':'assistant','msg':'请输入文本或文件以进行转换'})
    messageItem = computed(()=>store.state.message.sendMessage).value
  }
})

onUnmounted(()=>{
  store.commit('clearMsg')
  messageItem = computed(() => store.state.message.sendMessage).value
})

</script>

<template>
  <Panel />
  <div class="work-area">
    <el-tabs tab-position="left" v-model="activeName" class="demo-tabs" @tab-click="handleClicktab">
      <el-tab-pane label="文本转写" name="first" class="convert-text">
        <el-scrollbar height="580px">
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
          <el-upload
            ref="uploadRef"
            class="upload-demo"
            multiple
            accept=".txt"
            action="http://localhost:5000/textfileupload"
            :limit="1"
            :on-success="handleSuccess"
            :show-file-list="false"
          >
            <el-button type="primary" circle size="large">
              <el-icon><FolderOpened /></el-icon>
            </el-button>
          </el-upload>
          <el-button type="info" circle size="large" @click="saveFile">
            <el-icon><Download /></el-icon>
          </el-button>
          <el-button type="danger" circle size="large" @click="clearMessage">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
      </el-tab-pane>
      <el-tab-pane label="文本翻译" name="second" class="translate-text">
        <el-scrollbar height="580px">
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
          <el-upload
            ref="uploadRef"
            class="upload-demo"
            multiple
            accept=".txt"
            action="http://localhost:5000/textfileupload"
            :limit="1"
            :on-success="handleSuccess"
            :show-file-list="false"
          >
            <el-button type="primary" circle size="large">
              <el-icon><FolderOpened /></el-icon>
            </el-button>
          </el-upload>
          <el-button type="info" circle size="large" @click="saveFile">
            <el-icon><Download /></el-icon>
          </el-button>
          <el-button type="danger" circle size="large" @click="clearMessage">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
      </el-tab-pane>
      <el-tab-pane label="文本摘要" name="third" class="summarize-text">
        <el-scrollbar height="580px">
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
          <el-upload
            ref="uploadRef"
            class="upload-demo"
            multiple
            accept=".txt"
            action="http://localhost:5000/textfileupload"
            :limit="1"
            :on-success="handleSuccess"
            :show-file-list="false"
          >
            <el-button type="primary" circle size="large">
              <el-icon><FolderOpened /></el-icon>
            </el-button>
          </el-upload>
          <el-button type="info" circle size="large" @click="saveFile">
            <el-icon><Download /></el-icon>
          </el-button>
          <el-button type="danger" circle size="large" @click="clearMessage">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.work-area {
    padding-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 800px;
}

.convert-text {
  border: 1px solid #c6ced5;
  border-radius: 4px;
  width: 800px;
}

.translate-text {
  /* background-color: deeppink; */
  border: 1px solid #c6ced5;
  border-radius: 4px;
  width: 800px;
}

.summarize-text {
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

.upload-demo {
  padding: 0px 10px 0px 10px
}
</style>