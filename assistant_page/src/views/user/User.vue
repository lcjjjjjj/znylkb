<script lang="ts" setup>
import Panel from '@/components/Panel.vue';
import { ref, reactive, computed } from 'vue';
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useStore } from 'vuex';
import { userUpdate } from '@/api';

const ruleFormRef = ref<FormInstance>()
const store = useStore()

const userItem = computed(() => store.state.user.userInfo).value
console.log(userItem)

const ruleForm = reactive({
    username: userItem[0]['username'],
    pass: '',
    checkpass: ''
})

const validatePass = (rule: any, value: any, callback: any) => {
    if(value === ''){
        callback(new Error('请输入密码'))
    }
    else{
        if(ruleForm.checkpass !== ''){
            if(!ruleFormRef.value) return
            ruleFormRef.value.validateField('checkpass')
        }
        callback()
    }
}

const validatePass2 = (rule: any, value: any, callback: any) => {
    if(value === ''){
        callback(new Error('请再次输入密码'))
    }
    else if(value !== ruleForm.pass){
        callback(new Error('两次输入的密码不匹配'))
    }
    else{
        callback()
    }
}

const rules = reactive<FormRules<typeof ruleForm>>({
    pass: [{required: true, validator: validatePass, trigger: 'blur' }],
    checkpass: [{required: true, validator: validatePass2, trigger: 'blur' }]
})

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
      userUpdate({username: ruleForm.username, password: ruleForm.pass}).then((res) => {
        if(res.data.msg === 'success'){
            ElMessage.success('Update successifully!')
        }
        else
            ElMessage.error('Unkonwn error!')
      })
    } else {
      console.log('error submit!')
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}

</script>

<template>
    <Panel />
    <div class="avatar">
        <el-avatar size="large" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
    </div>
    <div class="form-area">
        <el-form
            ref="ruleFormRef"
            style="max-width: 600px;"
            :model="ruleForm"
            status-icon
            :rules="rules"
            label-width="auto"
            class="demo-ruleForm"    
        >   
            <el-form-item label="用户名" prop="username">
                <el-input disabled v-model="ruleForm.username" />
            </el-form-item>
            <el-form-item label="密码" prop="pass">
                <el-input v-model="ruleForm.pass" type="password" autocomplete="off" />
            </el-form-item>
            <el-form-item label="确认密码" prop="checkpass">
                <el-input v-model="ruleForm.checkpass" type="password" autocomplete="off" />
            </el-form-item>
            <div class="button-container">
                <el-form-item>
                    <el-button type="primary" @click="submitForm(ruleFormRef)">提交</el-button>
                    <el-button @click="resetForm(ruleFormRef)">重置</el-button>
                </el-form-item>
            </div>
        </el-form>
    </div>
</template>

<style scoped>
.form-area {
    padding-top: 25px;
    display: flex;
    justify-content: center;
}

.button-container {
    display: flex;
    justify-content: flex-end;
}

.avatar {
    padding-top: 25px;
    display: flex;
    justify-content: center;
}
</style>