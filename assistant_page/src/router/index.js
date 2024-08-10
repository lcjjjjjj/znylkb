import { createRouter, createWebHistory } from 'vue-router'
import Main from '../views/Main.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
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
            id: '2', name: '文本处理', icon: 'document', path: '/textsum', describe: '文本处理，上传文本或直接输入文本，可将口语化的文本转换为书面文本。'
          },
          component: () => import('../views/textsum/Textsum.vue')
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
  if (from.name === undefined && to.path !== '/' && to.path !== '/test') {
    next('/');
  } else {
    next();
  }
})

export default router
