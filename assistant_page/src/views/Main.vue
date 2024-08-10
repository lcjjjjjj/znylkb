<script setup>
import Menu from '../components/Menu.vue'
import Header from '../components/Header.vue'
import { RouterView, useRoute } from 'vue-router'
import { ref, onMounted } from "vue"
import TypeIt from 'typeit'
const route = useRoute()


onMounted(()=>{
  new TypeIt("#message",{
    strings: ["欢迎使用智能语录系统！"],
    speed: 300,
    lifeLike: true,
    loop: true,
    waitUntilVisible: true
  }).go()
})

</script>

<template>
    <div class="common-layout">
      <el-container>
        <Menu />
        <el-container>
          <el-header class="header-manu"><Header /></el-header>
          <el-main>
            <div v-show="route.path === '/'" id="message" class="helloMessage"></div>
            <RouterView />
          </el-main>
        </el-container>
      </el-container>
    </div>
</template>

<style scopd>

.common-layout {
  height: 100%;
}

.el-container {
    height: 100%;
}


.helloMessage {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 60px;
  font-weight: bold;
  height: 100%;
  color: #545c64;
}

</style>