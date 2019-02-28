import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'

import DiskUserRate from '@/components/disk_use_rate'
import Home from '@/components/HelloWorld'

Vue.use(Router)
Vue.use(VueResource)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'temp home',
      component: Home
    },
    {
      path: '/system/disk_use_rate',
      name: 'disk_use_rate',
      component: DiskUserRate
    }
  ]
})
