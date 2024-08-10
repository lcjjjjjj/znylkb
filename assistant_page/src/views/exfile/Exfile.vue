<script setup>
import Panel from '@/components/Panel.vue';
</script>

<template>
    <Panel />
    <div class="app-area">
        <el-upload
            class="upload-demo"
            drag
            action=""
            multiple
            accept=".wav, .mp3"
            :limit="1"
        >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
                拖拽文件到此处 或 <em>点击上传</em>
            </div>
        </el-upload>
    </div>
</template>

<style scoped>
.app-area {
    padding-top: 15px;
    padding-bottom: 15px;
    padding-left: 25%;
    padding-right: 25%;
}
</style>