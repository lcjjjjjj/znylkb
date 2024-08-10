<script setup> 
import { useStore } from 'vuex';
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
    
const store = useStore()
const route = useRoute()
const selectedItem = computed(() => store.state.menu.selectMenu).value
const title = ref('')
const desc = ref('')

console.log(store.state)

const showPanel = (route) => {
    const index = selectedItem.findIndex((item) => item.path === route.path)
    title.value = selectedItem[index].name
    desc.value = selectedItem[index].describe
}

showPanel(route)
</script>

<template>
    <div class="panel-heading">
        <div class="panel-lead">
            <div class="title">{{ title }}</div>
            <p class="description">{{ desc }}</p>
        </div>
    </div>
</template>

<style scoped>
.panel-heading{
    padding: 15px;
    background: #e8edf0;
    border-color: #e8edf0;
    position: relative;
}

.penal-lead {
    font-size: 14px;
}

.title {
    font-weight: bold;
    font-style: normal;
}

.description {
    margin-top: 5px;
}
</style>