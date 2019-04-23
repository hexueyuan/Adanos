<template>
  <el-menu class="smws-aside-menu" default-active="2">
    <el-submenu index="1">
      <template slot="title">
        <span style="font-size: 1vw">系统监控</span>
      </template>
      <el-menu-item-group style="background-color:#f4f4f4;">
      <el-menu-item index="1-1"><router-link class="router-link" to="/cpuPage">CPU数据</router-link></el-menu-item>
      <el-menu-item index="1-2"><router-link class="router-link" to="/memoryPage">内存数据</router-link></el-menu-item>
      <el-menu-item index="1-3"><router-link class="router-link" to="/diskPage">磁盘数据</router-link></el-menu-item>
      </el-menu-item-group>
    </el-submenu>
    <el-menu-item index="2">
      <span slot="title"><router-link  style="font-size: 1vw;text-decoration:none;color: black;" to="/fileSystemPage">文件系统</router-link></span>
    </el-menu-item>
    <el-menu-item index="3">
      <span slot="title"><router-link  style="font-size: 1vw;text-decoration:none;color: black;" to="/TestPage">测试页面</router-link></span>
    </el-menu-item>
    <el-menu-item index="4">
      <span slot="title"><router-link  style="font-size: 1vw;text-decoration:none;color: black;" to="/watcherPage">开发页面</router-link></span>
    </el-menu-item>
    <el-menu-item index="5">
      <span slot="title"><router-link  style="font-size: 1vw;text-decoration:none;color: black;" to="/dashboardTest">测试仪表盘</router-link></span>
    </el-menu-item>
    <el-menu-item index="6">
      <span slot="title"><router-link  style="font-size: 1vw;text-decoration:none;color: black;" to="/linechartTest">测试折线图</router-link></span>
    </el-menu-item>
    <el-menu-item index="7">
      <span slot="title"><router-link  style="font-size: 1vw;text-decoration:none;color: black;" to="/pieTest">测试饼状图</router-link></span>
    </el-menu-item>
    <el-menu-item index="8">
      <span slot="title"><router-link  style="font-size: 1vw;text-decoration:none;color: black;" to="/cardTest">测试卡片组件</router-link></span>
    </el-menu-item>
    <el-menu-item index="9">
      <span slot="title"><router-link  style="font-size: 1vw;text-decoration:none;color: black;" to="/mutillinechartTest">测试多组折线图</router-link></span>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  mounted() {
    this.$socket.emit('cpuDataRequest')
    this.$socket.emit('diskDataRequest')
    this.$socket.emit('memoryDataRequest')
  },
  sockets: {
    onDiskData(data) {
      this.$store.commit('updateDiskData', [data])
    },
    onCPUData(data) {
      this.$store.commit('updateCPUData', [data])
    },
    onMemoryData(data) {
      this.$store.commit('updateMemoryData', [data])
    }
  }
}
</script>

<style lang="scss">
.router-link {
  text-decoration:none;
  color: black;
  font-size: 1vw;
  background-color: #f4f4f4;
}
.smws-aside-menu {
  border: 5px;
  color: black;
  background-color: #f4f4f4;
}
</style>
