<script setup lang="ts">
import { useRouter } from 'vue-router';
import { ref, reactive, nextTick } from 'vue';
import { ElMessage, FormInstance, FormRules } from 'element-plus';
import type { TabsPaneContext } from 'element-plus';
import { userOption } from '@/api';
import { useStore } from 'vuex';

const router = useRouter()
const store = useStore()

const loginFunction = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
      console.log(ruleForm.username,ruleForm.password)
      userOption({task: 'login', username: ruleForm.username, password: ruleForm.password}).then((res) => {
        console.log(res)
        if(res.data.msg === 'success'){
          store.commit('addInfo',{'username':ruleForm.username})
          router.push('./main')
        }
        else
          ElMessage.error('Username or password error')
      })
    } else {
      console.log('error submit!')
    }
  })
}

const registerFunction = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
      userOption({task: 'register', username: ruleForm_re.username, password: ruleForm_re.pass}).then((res)=>{
        console.log(res)
        if(res.data.msg === 'success'){
          ElMessage.success('Register successifully!')
          setTimeout(() => window.location.reload(),1000)
          
        }
        else if(res.data.msg === 'failed')
          ElMessage.error('Username already exist!')
        else
          ElMessage.error('Unkown error!')
      })
    } else {
      console.log('error submit!')
    }
  })
}

const commonLayout = {
  'background-image': 'url("https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg")',
  'background-size': 'cover' 
}

// 创建响应式表单数据
const ruleFormRef = ref<FormInstance>()

// 表单内容
const ruleForm = reactive({
  'username': '',
  'password': ''
})

const rules = reactive<FormRules<typeof ruleForm>>({
  'username': [{'required': true, 'message': '请输入用户名', 'trigger': 'blur'}],
  'password': [{'required': true, 'message': '请输入密码', 'trigger': 'blur'}]
})

const activeName = ref('first')

const handleClicktab = (tab: TabsPaneContext, event: Event) => {
  console.log(tab.props.name, event)
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}

const ruleFormRef_re = ref<FormInstance>()

const ruleForm_re = reactive({
    username: '',
    pass: '',
    checkpass: ''
})

const validatePass = (rule: any, value: any, callback: any) => {
    if(value === ''){
        callback(new Error('请输入密码'))
    }
    else{
        if(ruleForm_re.checkpass !== ''){
            if(!ruleFormRef_re.value) return
            ruleFormRef_re.value.validateField('checkpass')
        }
        callback()
    }
}

const validatePass2 = (rule: any, value: any, callback: any) => {
    if(value === ''){
        callback(new Error('请再次输入密码'))
    }
    else if(value !== ruleForm_re.pass){
        callback(new Error('两次输入的密码不匹配'))
    }
    else{
        callback()
    }
}

const rules_re = reactive<FormRules<typeof ruleForm_re>>({
    username: [{required: true, message:'请输入用户名', trigger: 'blur'}],
    pass: [{required: true, validator: validatePass, trigger: 'blur' }],
    checkpass: [{required: true, validator: validatePass2, trigger: 'blur' }]
})
</script>

<template>
  <div class="common-layout" 
  :style="commonLayout">
    <el-container >
      <el-main class="main"></el-main>
      <el-aside class="aside">
        <div class="login-form">
          <p class="form-title">智能语录系统</p>
          <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClicktab">
            <el-tab-pane label="账号密码登录" name="first">
              <el-form
              ref="ruleFormRef"
              style="max-width: 350px;"
              :model="ruleForm"
              status-icon
              :rules="rules"
              label-width="auto"
              class="login-ruleForm">
                <el-form-item label="用户名" prop="username" class="form-item-username">
                  <el-input v-model="ruleForm.username" />
                </el-form-item>
                <el-form-item label="密码" prop="password" class="form-item-password">
                  <el-input v-model="ruleForm.password" type="password" />
                </el-form-item>
              </el-form>
              <div class="button-container">
                <el-button type="success" circle size="large" @click="loginFunction(ruleFormRef)" class="button-check">
                  <el-icon><Check /></el-icon>
                </el-button>
                <el-button type="danger" circle size="large" @click="resetForm(ruleFormRef)" class="button-close">
                  <el-icon><Close /></el-icon>
                </el-button>
              </div>
            </el-tab-pane>
            <el-tab-pane label="User Register" name="second">
              <el-form
                ref="ruleFormRef_re"
                style="max-width: 350px;"
                :model="ruleForm_re"
                status-icon
                :rules="rules_re"
                label-width="auto"
                class="login-ruleForm"    
              >   
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="ruleForm_re.username" />
                </el-form-item>
                <el-form-item label="密码" prop="pass">
                    <el-input v-model="ruleForm_re.pass" type="password" autocomplete="off" />
                </el-form-item>
                <el-form-item label="确认密码" prop="checkpass">
                    <el-input v-model="ruleForm_re.checkpass" type="password" autocomplete="off" />
                </el-form-item>
                <div class="button-container">
                  <el-form-item>
                    <el-button type="success" circle size="large" @click="registerFunction(ruleFormRef_re)" class="button-check">
                      <el-icon><Check /></el-icon>
                    </el-button>
                    <el-button type="danger" circle size="large" @click="resetForm(ruleFormRef_re)" class="button-close">
                      <el-icon><Close /></el-icon>
                    </el-button>
                  </el-form-item>
                </div>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-aside>
    </el-container>
  </div>
</template>

<style scoped>
  .aside {
    /* background-color: antiquewhite; */
    width: 500px;
    background-color: rgba(84, 92, 100, 0.5);
    display: flex;
    flex-direction: column;
    justify-content: center; /*垂直居中*/
    align-items: center; /*水平居中*/
  }
  /* .common-layout {
    background-image: url('https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg');
    background-size: cover;
  } */
  .login-form {
    width: 450px;
    height: 500px;
    background-color: rgb(255,255,255);
    border-radius: 2%;
    display: flex;
    flex-direction: column;
    align-items: center;
    
  }
  /* .main {
    background-color: aqua;
  } */
  .button-container {
    width: 350px;
    display: flex;
    flex-direction: row;
    justify-content: center ;
  }
  .form-title {
    display: grid;
    font-size: 25px;
    /* 垂直居中 */
    place-items: center; 
    /* 水平居中 */
    text-align: center;
    font-weight: bold;
    color: #545c64;
    height: 100px;
  }
  .demo-tabs  {
  padding: 32px;
  color: #ffd04b;
  font-size: 32px;
  font-weight: 600;
  }
  .el-tabs {
    padding: 0px;
  }
  .form-item-username {
    margin-top: 36px;
    margin-bottom: 36px;
  }
  .form-item-password {
    margin-bottom: 72px;
  }
  .button-check {
    margin-right: 32px;
  }
  .button-close {
    margin-left: 32px;
  }
</style>
