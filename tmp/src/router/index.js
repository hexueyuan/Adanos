import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/components/pages/Home'
import Diskpage from '@/components/pages/Diskpage'
import CPUpage from '@/components/pages/CPUpage'
import Memorypage from '@/components/pages/Memorypage'
import FileSystempage from '@/components/pages/FileSystemGUI'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/diskPage',
      name: 'diskPage',
      component: Diskpage
    },
    {
      path: '/cpuPage',
      name: 'cpuPage',
      component: CPUpage
    },
    {
      path: '/memoryPage',
      name: 'memoryPage',
      component: Memorypage
    },
    {
      path: '/fileSystemPage',
      name: 'fileSystemPage',
      component: FileSystempage
    }
  ]
})
