<template>
    <el-container class="app-all" direction="vertical">
      <el-header class="app-header">
        <Header></Header>
      </el-header>
      <el-container class="app-context" direction="horizontal">
        <el-aside class="app-aside">
          <Aside></Aside>
        </el-aside>
        <el-main class="app-main">
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
</template>

<script>
import Header from './components/base/Header'
import Aside from './components/base/Aside'

export default {
  name: 'App',
  components: {
    Header,
    Aside
  }
}
</script>

<style lang="scss">
  .app-all {
    height: 100%;
    width: 100%;
    .app-header {
      background-color: rgb(71, 82, 82);
      height: 5% !important;
    }
    .app-context {
      height: 95% !important;
      .app-aside {
        background-color:#545c64;
        height: 100%;
        width: 15% !important;
      }
      .app-main {
        background-color: rgb(255, 255, 255);
        height: 100%;
        width: 85% !important;
        margin: 0px;
        padding: 0px;
      }
    }
  }
</style>
