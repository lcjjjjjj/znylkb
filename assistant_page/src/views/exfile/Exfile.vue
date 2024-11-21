<script setup>
import Panel from '@/components/Panel.vue';
import { ElMessageBox, ElMessage } from 'element-plus';
import { saveFile, deleteFile } from '@/api';
import { ref, computed } from 'vue'
import { useStore } from 'vuex'

const value = ref('')

const options = [
  {
    value: 'mp3',
    label: 'mp3',
  },
  {
    value: 'wav',
    label: 'wav'
  }
   
]

const store = useStore()
const userItem = computed(() => store.state.user.userInfo).value
console.log(userItem)


const beforeUpload = (file) => {
    const filetype = file.name.split('.').pop().toLowerCase()
    if (value.value === ''){
        ElMessageBox.alert('请先选择转换类型',{confirmButtonText: '确定'}) 
        return false
    }
    else if (value.value === filetype){
        ElMessageBox.alert('无法转换相同格式的文件',{confirmButtonText: '确定'}) 
        return false
    }
    else if(value.value !== 'mp3' && value.value !== 'wav' ){
        ElMessageBox.alert('请上传格式正确的文件',{confirmButtonText: '确定'}) 
        return false
    }
    else{
        return true
    }
}

const handleExceed = (files, uploadFiles) => {
    console.log('限制上传', files, uploadFiles)
    ElMessageBox.alert('只能上传一个文件，如有需要请删除上一个文件再进行上传','温馨提示',{confirmButtonText: '确定',})
}

const handleRemove = (file,fileList) => {
    console.log(file)
    console.log(fileList)
    deleteFile().then((res) => {
        console.log(res.data.msg)
    })
}

const handleSavefile = () => {
    if (value.value ==''){
        ElMessageBox.alert('请先上传文件',{confirmButtonText: '确定'}) 
    }
    if (value.value == 'wav'){
        saveFile({task: 'wav', username: userItem[0]['username']}).then((res) => {
            if (res.data.msg === 'Done'){
                ElMessage.success('保存成功')
            }
            else{
                ElMessageBox.alert('请先上传文件',{confirmButtonText: '确定'})
            }
        })
    }
    else if(value.value == 'mp3'){
        saveFile({task: 'mp3', username: userItem[0]['username']}).then((res) => {
            console.log(res)
            if (res.data.msg === 'Done'){
                ElMessage.success('保存成功')
            }
            else{
                ElMessageBox.alert('请先上传文件',{confirmButtonText: '确定'})
            }
        })
    }
}
</script>

<template>
    <Panel />
    <div class="app-area">
        <el-upload
            class="upload-demo"
            drag
            action="http://localhost:5000/convert"
            multiple
            accept=".wav, .mp3"
            :before-upload="beforeUpload"
            :on-exceed = "handleExceed"
            @remove = "handleRemove"
            :limit="1"
        >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
                拖拽文件到此处 或 <em>点击上传</em>
            </div>
        </el-upload>
    </div>
    <div class="buttons">
        <div class="buttons-left">
            <el-select
                v-model="value"
                placeholder="选择需要转成的文件格式"
                size="large"
                style="width: 240px"
            >
                <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                />
            </el-select>
        </div>
        <div class="buttons-right">
            <el-button type="success" round @Click="handleSavefile">保存</el-button>
        </div>
    </div>
</template>

<style scoped>
.app-area {
    padding-top: 5%;
    padding-bottom: 15px;
    padding-left: 25%;
    padding-right: 25%;
}

.buttons {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-left: 25%;
    padding-right: 25%;
}

.buttons-left {
    display: flex;
    justify-content: flex-end;
}

.buttons-right {
    display: flex;
    justify-content: flex-start;
}
</style>