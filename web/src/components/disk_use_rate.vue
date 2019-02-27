<template>
<el-table :data="tableData" style="width: 100%">
  <el-table-column prop="mount_point" label="挂载点" width="180"></el-table-column>
  <el-table-column prop="use_rate" label="使用率" width="180"></el-table-column>
  <el-table-column prop="date" label="日期" width="180"></el-table-column>
  <el-table-column prop="time" label="时间"></el-table-column>
</el-table>
</template>

<script>
export default {
  data () {
    return {
      tableData: [],
      isCollapse: false
    }
  },
  created: function () {
    this.get_disk_use_rate_data()
  },
  methods: {
    get_disk_use_rate_data: function () {
      var that = this
      this.$http.get('http://localhost:5000/smowsAPI/disk_use_rate').then(function (data) {
        that.tableData = data.body.data['use_rate']['/']
      })
    }
  }
}
</script>

<style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    height: 800px;
  }
</style>
