<template>
<div>
  <el-row>
    <el-col :span="18">
      <el-select v-model="selectMountPoint" placeholder="请选择挂载点">
        <el-option v-for="item in tableData.mount_points" :key="item" :value="item" :label="item" :selectMountPoint="item"></el-option>
      </el-select>
    </el-col>
    <el-col :span="6">
      <el-button @click="insert_data">插入数据</el-button>
    </el-col>
    <el-col :span="24" :push="1">
      <Table v-show="isSelect" :table-property="tableProperty" :table-data="showData" :column-width="180"></Table>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="24">
      <LineChart :chart-data="chartData"></LineChart>
    </el-col>
  </el-row>
</div>
</template>

<script>
import Table from './charts/Table'
import LineChart from './charts/LineChart'

export default {
  components: {
    Table,
    LineChart
  },
  data () {
    return {
      tableProperty: [
        {
          prop: "mount_point",
          label: "挂载点"
        },
        {
          prop: "use_rate",
          label: "使用率"
        },
        {
          prop: "timestamp",
          label: "时间"
        }
      ],
      tableData: {},
      isSelect: false,
      selectMountPoint: "",
      showData: [],
      chartData: {
        title: { text: 'ECharts 入门示例' },
        tooltip: {},
        xAxis: {
          data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
        },
        yAxis: {},
        series: [{
          name: '销量',
          type: 'bar',
          data: [5, 20, 36, 10, 10, 20]
        }]
      }
    }
  },
  created: function () {
    this.get_disk_use_rate_data()
  },
  methods: {
    get_disk_use_rate_data: function () {
      var that = this
      this.$http.get('http://localhost:5000/smowsAPI/disk_use_rate').then(function (data) {
        that.tableData = data.body.data
      })
    },
    display_table_data: function () {
      this.isSelect = true
    },
    insert_data: function() {
      this.showData.push({"mount_point": "-", "use_rate": 12.34, "timestamp": 1234})
    }
  },
  watch: {
    selectMountPoint: function (val) {
      this.isSelect = true
      this.showData = this.tableData.use_rate[val]
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
