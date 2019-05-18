<template>
  <el-menu class="smws-aside-menu" default-active="2">
    <el-submenu index="1">
      <template slot="title">
        <span style="font-size: 1vw">系统监控</span>
      </template>
      <el-menu-item-group style="background-color:#f4f4f4;">
      <el-menu-item index="1-1"><router-link class="router-link" to="/Adanos/CPUPage">CPU数据</router-link></el-menu-item>
      <el-menu-item index="1-2"><router-link class="router-link" to="/Adanos/MemoryPage">内存数据</router-link></el-menu-item>
      <el-menu-item index="1-3"><router-link class="router-link" to="/Adanos/DiskPage">磁盘数据</router-link></el-menu-item>
      </el-menu-item-group>
    </el-submenu>
    <el-menu-item index="2">
      <span slot="title"><router-link  style="font-size: 1vw;text-decoration:none;color: black;" to="/Adanos/fileSystem">文件系统</router-link></span>
    </el-menu-item>
    <el-menu-item index="3">
      <span slot="title"><router-link  style="font-size: 1vw;text-decoration:none;color: black;" to="/Adanos/webssh">webssh</router-link></span>
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  mounted() {
    this.$socket.emit('connect')
  },
  sockets: {
    onNewData(data) {
      if (data.cpu.length != 0) {
        this.$store.commit('updateCPUData', data.cpu)
      }
      if (data.memory.length != 0) {
        this.$store.commit('updateMemoryData', data.memory)
      }
      if (data.disk.length != 0) {
        this.$store.commit('updateDiskData', data.disk)
      }
    }
  },
  destroyed() {
    this.$socket.emit('disconnect')
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
