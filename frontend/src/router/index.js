import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/components/pages/Home'
import Diskpage from '@/components/pages/Diskpage'
import CPUpage from '@/components/pages/CPUpage'
import Memorypage from '@/components/pages/Memorypage'
import FileSystempage from '@/components/pages/FileSystemGUI'
import TESTpage from '@/components/pages/TESTpage'
import Watcherpage from '@/components/pages/WatcherPage'
import dashboardTest from '@/components/pages/test/dashboardTest'
import linechartTest from '@/components/pages/test/linechartTest'
import pieTest from '@/components/pages/test/pieTest'
import cardTest from '@/components/pages/test/cardTest'
import mutillinechartTest from '@/components/pages/test/mutillinechartTest'

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
    },
    {
      path: '/TestPage',
      name: 'TestPage',
      component: TESTpage
    },
    {
      path: '/watcherPage',
      name: 'watcherPage',
      component: Watcherpage
    },
    {
      path: '/dashboardTest',
      name: 'dashboardTest',
      component: dashboardTest
    },
    {
      path: '/linechartTest',
      name: 'linechartTest',
      component: linechartTest
    },
    {
      path: '/pieTest',
      name: 'pieTest',
      component: pieTest
    },
    {
      path: '/cardTest',
      name: 'cardTest',
      component: cardTest
    },
    {
      path: '/mutillinechartTest',
      name: 'mutillinechartTest',
      component: mutillinechartTest
    }
  ]
})
