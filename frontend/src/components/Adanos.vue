<template>
    <el-container id="myapp" direction="vertical">
      <el-header id="app-header">
        <Header/>
      </el-header>
      <el-container id="app-context" direction="horizontal">
        <el-aside id="app-aside">
          <Aside/>
        </el-aside>
        <el-main id="app-page">
          <Page/>
        </el-main>
      </el-container>
    </el-container>
</template>

<script>
import Header from './base/Header'
import Aside from './base/Aside'
import Page from './base/Page'

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
