<script setup>
import Panel from '@/components/Panel.vue';
import { ref } from 'vue';
import { ElMessageBox, textProps } from 'element-plus';
import { postSignal, postKeep, postClear } from '@/api';

const result = ref('');
const flag = ref('keep')
const timer = ref(null)
let count = 0


const handleExceed = (files, uploadFiles) => {
    console.log('限制上传', files, uploadFiles)
    ElMessageBox.alert('只能上传一个文件，如有需要请删除上一个文件再进行上传','温馨提示',{confirmButtonText: '确定',})
}

const handleSuccess = (res, file, fileList) => {
    console.log(res)
    result.value = res.msg
}

const onClicksave = () => {
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
            <el-button type="primary" round @Click="onClickstart">开始</el-button>
            <el-button type="warning" round @Click="onClickstop">停止</el-button>
            <el-button type="danger" round @Click="onClickretry">重试</el-button>
            <el-button type="success" round @Click="onClicksave">保存</el-button>
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