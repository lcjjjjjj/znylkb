import { createRouter, createWebHistory } from 'vue-router'
import Main from '../views/Main.vue'

// 创建路由器
const router = createRouter({
  // 路由工作模式
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/main',
      name: 'main',
      component: Main,
      children: [
        {
          path:'/asr',
          name: 'asr',
          meta: {
            id: '1', name: '语音识别', icon: 'Microphone', path: '/asr' ,describe: '语音识别，选择需要进行识别的语言，可上传音频文件或直接录音，识别结果将显示在页面上。'
          },
          component: () => import('../views/asr/ASR.vue')
        },
        {
          path: '/textsum',
          name: 'textsum',
          meta: {
            id: '2', name: '文本转写', icon: 'document', path: '/textsum', describe: '文本转写，上传文本或直接输入文本，可将口语化的文本转换为书面文本。'
          },
          component: () => import('../views/textsum/Textsum.vue')
        },
        {
          path: '/exfile',
          name: 'exfile',
          meta: {
            id: '3', name: '音频转换', icon: 'Refresh', path: '/exfile', describe: '音频转换，上传音频文件，可选择指定格式保存。'
          },
          component: () => import('../views/exfile/Exfile.vue')
        },
        {
          path: '/file',
          name: 'file',
          meta: {
            id: '4', name: '文件管理', icon: 'Folder', path: '/file', describe: '文件管理，管理生成的文本和音频文件。'
          },
          component: () => import('../views/file/FileManager.vue')
        },
        {
          path: '/user',
          name: 'user',
          meta: {
            id: '5', name: '账号管理', icon: 'User', path: '/user', describe: '账号管理，修改账户的基本信息。'
          },
          component: () => import('../views/user/User.vue')
        }
      ]
    },
    {
      path: '/test',
      name: 'test',
      component: () => import('../views/Test.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  // 检查页面是否刷新
  console.log(to.path)
  console.log(from.name)
  if (from.name === undefined && to.path !== '/' && to.path !== '/main') {
    next('/');
  } else {
    next();
  }
})

export default router
