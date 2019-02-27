import Vue from 'vue'
import Router from 'vue-router'
import DiskUserRate from '@/components/disk_use_rate'
import VueResource from 'vue-resource'

Vue.use(Router)
Vue.use(VueResource)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'temp home',
      component: DiskUserRate
    },
    {
      path: '/system/disk_use_rate',
      name: 'disk_use_rate',
      component: DiskUserRate
    }
  ]
})
