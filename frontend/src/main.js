import Vue from 'vue'
import ElementUI from 'element-ui'
import Main from '@/main.vue'
import VueResource from 'vue-resource'
import VueQuillEditor from 'vue-quill-editor'

import 'element-ui/lib/theme-chalk/index.css';
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(VueResource)
Vue.use(VueQuillEditor)

new Vue({
  render: h => h(Main),
}).$mount('#app')
