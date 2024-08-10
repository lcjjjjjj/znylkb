<script setup>
import { useStore } from 'vuex';
import { computed } from 'vue'; 
import { useRoute, useRouter } from 'vue-router';
//取得store实例
const store = useStore()
const selectedItem = computed(() => store.state.menu.selectMenu)
//当前的路由对象
const route = useRoute()
const router = useRouter()
//实现关闭Tab功能
const closeTab = (item, index) => {
    store.commit("closeMenu", item)
    if (route.path !== item.path) {
        return
    }
    const selectedItemData = selectedItem.value
    if (index === selectedItemData.length){
        if (!selectedItemData.length){
            router.push('/')
        }
        else{
            router.push({path: selectedItemData[index - 1].path})
        }
    }
    else{
        router.push({path: selectedItemData[index].path})
    }
}
</script>

<template>
    <div class='header-container'>
        <div class="header-left flex-box">
            <el-icon class="icon" size=20 @click="store.commit('collapseMenu')"><Fold /></el-icon>
            <ul class="flex-box">
                <!-- :class 设置条件效果显示 -->
                <li v-for="(item, index) in selectedItem" :key="item.path" class="top-tab flex-box" :class="{selected: route.path === item.path}">
                    <el-icon size="15"><component :is="item.icon" /></el-icon>
                    <router-link class="text flex-box" :to="{path: item.path}">{{ item.name }}</router-link>
                    <el-icon size="15" class="close" @click="closeTab(item, index)"><Close /></el-icon>
                </li>
            </ul>
        </div>
        <div class="header-right">
            <el-dropdown>
                <div class="el-dropdown-link flex-box">
                    <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
                    <p class="username">admin</p>
                </div>
                <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item>退出登录</el-dropdown-item>
                </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </div>
</template>

<style scoped>

.flex-box {
    display: flex;
    align-items: center;
}

.header-container{
    display: flex;
    align-items: center;
    height: 100%;
    justify-content: space-between;
    background-color: #fff;
    padding-right: 25px;
}

.icon {
    width: 60px;
    height: 100%;
}

.icon:hover {
    cursor: pointer;
    background-color: #f5f5f5;
    color: #ffd04b;
}

.header-left{
    height: 100%;
}

.username {
    margin-left: 10px;
}

.top-tab {
    padding: 0 10px;
    height: 100%;
    .close {
        visibility: hidden;
    }
}

/* 设置触碰事件 */
.top-tab:hover {
    background-color: #f5f5f5;
    color: #ffd04b;
    .close {
        visibility: inherit;
        cursor: pointer;
        color: #ffd04b;
    }
    a {
        color: #ffd04b;
    }
}

.text {
    margin: 0 5px;
}

a {
    height: 100%;
    color: #333;
    font-size: 15px;
}

ul {
    height: 100%;
}

.selected{
    background-color: #f5f5f5;
    a {
        color: #ffd04b;
    }
    i {
        color: #ffd04b;
    }
}
</style>