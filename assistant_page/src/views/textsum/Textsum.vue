<script setup>
import Panel from '@/components/Panel.vue';
import { ElMessageBox } from 'element-plus';
import { postText } from '@/api';
import { ref } from 'vue'
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

</script>

<template>
    <Panel />
    <div class="textsum-area">
        <el-input
            v-model="textarea"
            style="width: 45%;"
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
            style="width: 45%;"
            :rows="13"
            type="textarea"
            placeholder="改写结果"
        />
    </div>
</template>

<style scoped>
.textsum-area {
    display: flex;
    justify-content: center;
    padding: 10px;
    position: relative;
}

.buttons {
    display: flex;
    justify-content: center;
    position: relative;
    padding: 15px;
}

</style>