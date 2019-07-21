import ElementUI from 'element-ui'
import Main from '@/main.vue'
import Vue from 'vue'
import VueResource from 'vue-resource'

import 'element-ui/lib/theme-chalk/index.css';

Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(VueResource)

new Vue({
  render: h => h(Main),
}).$mount('#app')