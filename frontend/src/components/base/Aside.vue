<template>
  <el-row class="tac">
    <el-col>
      <el-menu
      default-active="2"
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose"
      background-color="#464646"
      text-color="#fff"
      style="border-right-width:0px;">
      <el-submenu index="1">
        <template slot="title">
          <span style="font-size: 1.5vw">系统监控</span>
        </template>
        <el-menu-item-group>
        <el-menu-item index="1-1"><router-link class="router-link" to="/cpuPage">CPU数据</router-link></el-menu-item>
        <el-menu-item index="1-2"><router-link class="router-link" to="/memoryPage">内存数据</router-link></el-menu-item>
        <el-menu-item index="1-3"><router-link class="router-link" to="/diskPage">磁盘数据</router-link></el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-menu-item index="2">
        <span slot="title"><router-link  style="font-size: 1.5vw;text-decoration:none;color: #fff;" to="/fileSystemPage">文件系统</router-link></span>
      </el-menu-item>
      <el-menu-item index="3">
        <span slot="title"><router-link  style="font-size: 1.5vw;text-decoration:none;color: #fff;" to="/TestPage">测试页面</router-link></span>
      </el-menu-item>
      <el-menu-item index="4">
        <span slot="title"><router-link  style="font-size: 1.5vw;text-decoration:none;color: #fff;" to="/watcherPage">开发页面</router-link></span>
      </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script>
export default {
  methods: {
    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    }
  }
}
</script>

<style lang="scss">
.router-link {
  text-decoration:none;
  color: #fff;
  font-size: 1vw;
}
</style>
