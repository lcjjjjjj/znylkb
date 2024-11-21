<script setup>
import Panel from '@/components/Panel.vue';
import { ref, computed } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';
import { postSignal, postKeep, postClear, saveFile } from '@/api';
import { useStore } from 'vuex';
import { postText } from '@/api';

const result = ref('');
const timer = ref(null)
const store = useStore()
const userItem = computed(() => store.state.user.userInfo).value
console.log(userItem)

const handleExceed = (files, uploadFiles) => {
    console.log('限制上传', files, uploadFiles)
    ElMessageBox.alert('只能上传一个文件，如有需要请删除上一个文件再进行上传','温馨提示',{confirmButtonText: '确定',})
}

const handleSuccess = (res, file, fileList) => {
    console.log(res)
    result.value = res.msg
}

const beforeUpload = (file) => {
    const filetype = file.name.split('.').pop().toLowerCase()
    if (filetype !== 'wav' && filetype !== 'mp3'){
        ElMessageBox.alert('请上传格式正确的文件',{confirmButtonText: '确定'}) 
        return false
    }
    else{
        return true
    }
}

const onClicksave = () => {
    if (result.value !== ''){
        const fileContent = result.value
        postText({text: fileContent,task: 'save', username: userItem[0]['username']}).then((res) => {
            console.log(res.data.msg)
            if(res.data.msg === 'Done'){
                ElMessage.success('保存成功')
            }
            else{
                ElMessage.error('保存失败')
            }
        })
    }
    else{
        ElMessageBox.alert('保存的内容不能为空','温馨提示',{confirmButtonText: '确定',})
    }
}


const onClickretry = () => {
    postClear({text: 'clear'})
    result.value = ''
}

const onClickstart = () => {
    postSignal({text: 'start'})
    timer.value = setInterval(()=>{
        postKeep({text: 'keep'}).then((res) => {
            console.log(res.data.msg)
            result.value = res.data.msg
        })
    },200)
}

const onClickstop = ()=>{
    postSignal({text: 'stop'})
    clearInterval(timer.value)
}

const onClicksave_a = () => {
    //通过get请求获得音频文件
    if(result.value !== ''){
        saveFile({task: 'asr', username: userItem[0]['username']}).then(res => {
            if(res.data.msg === 'Done'){
                ElMessage.success('保存成功')
            }
            else{
                ElMessage.error('保存失败，未检测到音频文件')
            }
        })
    }
    else{
        ElMessageBox.alert('未检测到音频文件','温馨提示',{confirmButtonText: '确定'})
    }
}
</script>

<template>
    <Panel />
    <div class="app-area">
        <el-upload
            class="upload-demo"
            drag
            action=" http://localhost:5000/upload"
            multiple
            accept=".wav, .mp3"
            :limit="1"
            :before-upload="beforeUpload"
            :on-exceed="handleExceed"
            :on-success="handleSuccess"
        >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
                拖拽文件到此处 或 <em>点击上传</em>
            </div>
        </el-upload>
    </div>
    <div class="button-area">
        <div class="left-area">
            
        </div>
        <div class="right-area">
            <el-button type="primary" round @Click="onClickstart">开始录音</el-button>
            <el-button type="warning" round @Click="onClickstop">停止</el-button>
            <el-button type="danger" round @Click="onClickretry">重试</el-button>
            <el-button type="success" round @Click="onClicksave_a">保存音频</el-button>
            <el-button type="success" round @Click="onClicksave">保存文本</el-button>
        </div>
    </div>
    <div class="result-area">
        <el-input
        v-model="result"
        style="width: 100%;"
        :rows="13"
        type="textarea"
        placeholder="识别结果"
        />
    </div>
</template>

<style scoped>
.app-area {
    padding-top: 15px;
    padding-left: 25%;
    padding-right: 25%;
    padding-bottom: 15px;
}

.button-area {
    display: flex;
    justify-content: space-between;
    padding-top: 15px;
    padding-left: 25%;
    padding-right: 25%;
    padding-bottom: 15px;
    
}

.result-area {
    
    padding-top: 15px;
    padding-left: 25%;
    padding-right: 25%;
    padding-bottom: 15px;
    
}
</style>