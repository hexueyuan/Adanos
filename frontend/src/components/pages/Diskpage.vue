<template>
  <div>
    <div style="height: 400px;width: 100%;margin-bottom: 30px;">
      <div id="disk-used-line-chart" style="height:100%;width:100%;"></div>
    </div>
    <el-table :data="devices" style="width:100%">
      <el-table-column prop="device_name" label="设备" width="250"></el-table-column>
      <el-table-column prop="mount_point" label="挂载点" width="250"></el-table-column>
      <el-table-column prop="fstype" label="文件系统" width="250"></el-table-column>
      <el-table-column prop="total" label="总量" width="250"></el-table-column>
      <el-table-column prop="used_rate" label="使用率"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import echarts from 'echarts'

export default {
  mounted() {
    this.init()
  },
  data() {
    return {
      devices: []
    }
  },
  computed: {
    diskData() {
      return this.$store.getters.diskData
    },
    tableData() {
      var data = []
      for (var device in this.$store.getters.diskData) {
        data.push(this.$store.getters.diskData[device][this.$store.getters.diskData[device].length -1])
      }
      return data
    }
  },
  watch: {
    diskData() {
      this.updateView()
    },
    tableData() {
      this.devices = this.tableData
    }
  },
  methods: {
    init() {
      this.updateView()
    },
    updateView() {
      if (this.usedLinechart == undefined) {
        this.usedLinechart = echarts.init(document.getElementById('disk-used-line-chart'))
        var initOption = JSON.parse(JSON.stringify(this.$conf.linechart_option))
        initOption.title = {
          text: '磁盘使用率实时数据',
          right: 'center',
          textStyle: {
            fontSize: 30
          }
        }
        initOption.grid = {
          x: '2%',
          y: '10%',
          x2: '2%',
          y2: '5%'
        }
        this.usedLinechart.setOption(initOption)
        this.usedLinechart.showLoading();
      } else {
        var option = {
          xAxis: {
            data: []
          },
          yAxis: {
            max: 100,
            min: 0,
            name: '使用率',
            type: 'value'
          },
          series: []
        }
        for (var device in this.$store.getters.diskData) {
          var conf = {
            name: device,
            data: [],
            type: 'line'
          }
          var timeList = []
          this.$store.getters.diskData[device].forEach(element => {
            timeList.push((new Date(element.timestamp * 1000)).toTimeString())
            conf.data.push(element.used_rate)
          })
          option.xAxis.data = timeList
          option.series.push(conf)
        }
        this.usedLinechart.setOption(option)
        this.usedLinechart.hideLoading()
      }
    }
  }
}
</script>

<style lang="scss">
</style>
