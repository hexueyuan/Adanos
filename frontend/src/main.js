// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueResource from 'vue-resource'
import store from './store'
import conf from './conf'

import VueSocketIO from 'vue-socket.io'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import '../static/icon/iconfont.css'

Vue.use(new VueSocketIO({
  connection: 'ws://localhost:5001',
  }), store)

Vue.use(ElementUI)
Vue.use(VueResource)
Vue.config.productionTip = false

Vue.http.options.emulateHTTP = true;
Vue.http.options.emulateJSON = true;

Vue.prototype.$conf = conf

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  conf,
  components: { App },
  template: '<App/>'
})