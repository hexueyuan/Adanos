<template>
  <el-row class="root-container">
      <el-col :span="24" class="root-header">
        <Header></Header>
      </el-col>
    <el-col class="root-context">
      <el-col :span="4">
        <Aside></Aside>
      </el-col>
      <el-col :span="20">
        <router-view></router-view>
      </el-col>
    </el-col>
  </el-row>
</template>

<script>
import Aside from './components/Aside'
import Header from './components/Header'

export default {
  components: {
    Aside,
    Header
  }
}
</script>

<style scoped lang="scss">
.root-container {
  position: absolute;
  top: 0px;
	bottom: 0px;
	width: 100%;
  .root-header {
    height: 70px;
    top: 0px;
    bottom: 0px;
		line-height: 100px;
		background: #13af66;;
		color:rgb(0, 0, 0);
  }
  .root-context {
    margin: 0px;
    border: 0px;
    padding: 0px;
    top: 0px;
    bottom: 0px;
  }
}
</style>
