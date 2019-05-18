<template>
    <router-view></router-view>
</template>

<script>
import Header from './components/base/Header'
import Aside from './components/base/Aside'
import Page from './components/base/Page'

export default {
  name: 'App',
  components: {
    Header,
    Aside,
    Page
  }
}
</script>

<style lang="scss">
html, body {
  font-size: 16px;
}
  #myapp {
    height: 100%;
    width: 100%;
    #app-header {
      background-color: #6db8b4;
      height: 7% !important;
    }
    #app-context {
      height: 93% !important;
      #app-aside {
        background-color:#f4f4f4;
        height: 100%;
        width: 10% !important;
      }
      #app-page {
        background-color: rgb(255, 255, 255);
        height: 100%;
        width: 90% !important;
        margin: 0px;
        padding: 0px;
      }
    }
  }
</style>
