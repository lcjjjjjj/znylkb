<script lang="ts" setup>

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

import {useRouter} from 'vue-router'
import { reactive, computed } from 'vue'
import { useStore } from 'vuex';

const router = useRouter()
console.log(router,'router')
const mapdata = reactive(router.options.routes[1].children)

const store = useStore()

const handleClick = (item) => {
    console.log(item,'item')
    store.commit('addMenu',item.meta)
    router.push(item.path)
}
const isCollapsed = computed(() => store.state.menu.isCollapsed)

</script>

<template>
    <el-menu
        :style="{ width: !isCollapsed ? '256px' : '64px' }"
        active-text-color="#ffd04b"
        background-color="#545c64"
        class="menu-container"
        default-active="0"
        text-color="#fff"
        :collapse="isCollapsed"
    >
        <p class="logo-lg">{{ !isCollapsed ? '智能语录' : 'IQ'}}</p>
        <template v-for="item in mapdata">
            <el-menu-item @click="handleClick(item)" v-if="item.path == '/asr'" :key="item.meta.id" :index="item.meta.id">
                <el-icon size="20">
                    <component :is="item.meta.icon"></component>
                </el-icon>
                <span>{{ item.meta.name }}</span>
            </el-menu-item>
            <el-menu-item @click="handleClick(item)" v-if="item.path == '/textsum'" :key="item.meta.id" :index="item.meta.id">
                <el-icon size="20">
                    <component :is="item.meta.icon"></component>
                </el-icon>
                <span>{{ item.meta.name }}</span>
            </el-menu-item>
            <el-menu-item @click="handleClick(item)" v-if="item.path == '/exfile'" :key="item.meta.id" :index="item.meta.id">
                <el-icon size="20">
                    <component :is="item.meta.icon"></component>
                </el-icon>
                <span>{{ item.meta.name }}</span>
            </el-menu-item>
            <el-menu-item @click="handleClick(item)" v-if="item.path == '/file'" :key="item.meta.id" :index="item.meta.id">
                <el-icon size="20">
                    <component :is="item.meta.icon"></component>
                </el-icon>
                <span>{{ item.meta.name }}</span>
            </el-menu-item>
            <el-menu-item @click="handleClick(item)" v-if="item.path == '/user'" :key="item.meta.id" :index="item.meta.id">
                <el-icon size="20">
                    <component :is="item.meta.icon"></component>
                </el-icon>
                <span>{{ item.meta.name }}</span>
            </el-menu-item>
        </template>
    </el-menu>
</template>

<style scoped>

.menu-container{
    height: 100%;
}

.logo-lg{
    display: grid;
    place-items: center;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    margin: 0;
    height: 60px;
    color: #545c64;
    background-color: #ffd04b;
}
</style>