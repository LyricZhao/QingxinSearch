<template>
  <div id="app">
    <ui ref="ui"> </ui>
  </div>
</template>

<script>
import ui from '@/components/ui.vue'
export default {
  name: 'app',
  components: {
    ui: ui
  },
  data() {
    return {}
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>