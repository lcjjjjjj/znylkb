<template>
  <Panel />
  <div class="table-area">
    <el-table :data="filterTableData" style="width: 100%">
      <el-table-column label="创建日期" prop="date" />
      <el-table-column label="文件名" prop="name" />
      <el-table-column label="文件大小" prop="size" />
      <el-table-column label="标签" prop="tag" />
      <el-table-column align="right">
        <template #header>
          <el-input v-model="search" size="small" placeholder="Type to search" />
        </template>
        <template #default="scope">
          <el-button size="small" type='primary' @click="handleSave(scope.$index, scope.row)">
            下载
          </el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import Panel from '@/components/Panel.vue'
import { computed, ref, onBeforeMount, onUpdated} from 'vue'
import { deleteFile, getFile, getFilelist, deleteTextFile } from '@/api';
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus';

interface File {
  date: string
  name: string
  size: string
  tag: string
}

const search = ref('')

const store = useStore()
const tableData = ref([])
const userItem = computed(() => store.state.user.userInfo).value
console.log(userItem)

const filterTableData = computed(() =>
  tableData.value.filter(
    (data) =>
      !search.value ||
      data.name.toLowerCase().includes(search.value.toLowerCase())
  )
)

const handleSave = (index: number, row: File) => {
  console.log(index, row)
  // index = 3 row json
  getFile({file: 'textfile', filename: row['name'], username: userItem[0]['username']}).then((res) => {
    console.log(res)
    const blob = new Blob([res.data])
    const link = document.createElement('a')
    const url = window.URL.createObjectURL(blob)
    link.href = url
    link.download=row['name']
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  })
}

const handleDelete = (index: number, row: File) => {
  console.log(index, row)
  deleteTextFile({filename: row['name'], username: userItem[0]['username']}).then((res) => {
    console.log(res.data.msg)
    if(res.data.msg === 'Done'){
      getFilelist({user: userItem[0]['username']}).then((res) => {
        console.log(res.data)
        tableData.value = []
        for (var i=0;i<res.data.length;i++){
          tableData.value.push(res.data[i])
        }
      })
      ElMessage.success('删除成功')
    }
    else{
      ElMessage.error('删除失败')
    }
  })
}

onBeforeMount(() => {
  return getFilelist({user: userItem[0]['username']}).then((res) => {
    console.log(res.data)
    for (var i=0;i<res.data.length;i++){
      tableData.value.push(res.data[i])
    }
  })
})

// onUpdated(() => {
//   return getFilelist({user: userItem[0]['username']}).then((res) => {
//     console.log(res.data)
//     for (var i=0;i<res.data.length;i++){
//       tableData.value.push(res.data[i])
//     }
//   })
// })

</script>

<style scoped>
.table-area {
  margin-top: 10px
}
</style>