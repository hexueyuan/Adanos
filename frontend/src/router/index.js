import Vue from 'vue'
import Router from 'vue-router'

import Login  from '@/components/base/Login'
import Adanos from '@/components/Adanos'

import Home from '@/components/pages/Home'
import DiskPage from '@/components/pages/Diskpage'
import CPUPage from '@/components/pages/CPUpage'
import MemoryPage from '@/components/pages/Memorypage'
import FileSystemPage from '@/components/pages/FileSystemGUI'

import webssh from '@/components/pages/webssh'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/Adanos',
      name: 'Adanos',
      component: Adanos,
      children: [
        {
          path: 'CPUPage',
          component: CPUPage
        },
        {
          path: 'MemoryPage',
          component: MemoryPage
        },
        {
          path: 'DiskPage',
          component: DiskPage
        },
        {
          path: 'fileSystem',
          component: FileSystemPage
        },
        {
          path: 'webssh',
          component: webssh
        }
      ]
    },
    {
      path: '/',
      name: 'Login',
      component: Login
    }
  ]
})
