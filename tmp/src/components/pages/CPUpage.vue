<template>
  <el-row style="height:100%;">
    <el-col :span="8" style="height:45vh;">
      <el-card style="height:100%">
        <Boardchart :chart-data="boardData" ></Boardchart>
      </el-card>
    </el-col>
    <el-col :span="8" style="height:45vh;">
      <el-card style="height:100%">
        <span style="width:100%; font-size:3vw">物理个数</span><br/>
        <span style="width:100%; color:green; font-size:5vw">{{ count.physics }}</span><br/>
        <span style="width:100%; font-size:3vw">逻辑个数</span><br/>
        <span style="width:100%; color:green; font-size:5vw">{{ count.logic }}</span><br/>
      </el-card>
    </el-col>
    <el-col :span="8" style="height:45vh;">
      <el-card style="height:100%">
        <span style="width:100%; font-size:2.5vw">用户态：</span><span style="width:100%; font-size:2.5vw; color: green">{{ useTime.user }}</span><br/>
        <span style="width:100%; font-size:2.5vw">系统态：</span><span style="width:100%; font-size:2.5vw; color: green">{{ useTime.system }}</span><br/>
        <span style="width:100%; font-size:2.5vw">IO等待：</span><span style="width:100%; font-size:2.5vw; color: orange">{{ useTime.io }}</span><br/>
        <span style="width:100%; font-size:2.5vw">硬中断：</span><span style="width:100%; font-size:2.5vw; color: orange">{{ useTime.irq }}</span><br/>
        <span style="width:100%; font-size:2.5vw">软中断：</span><span style="width:100%; font-size:2.5vw; color: orange">{{ useTime.sirq }}</span><br/>
      </el-card>
    </el-col>
    <el-col :span="24" style="height:47vh">
      <el-card style="height:100%">
        <Linechart :chart-data="chartData"></Linechart>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import Boardchart from '@/components/charts/Boardchart'
import Linechart from '@/components/charts/Linechart'

export default {
  components: {
    Boardchart,
    Linechart
  },
  data () {
    return {
      responseData: {
        data: {}
      },
      boardData: {},
      chartData: {},
      count: {
        physics: 0,
        logic: 0
      },
      useTime: {
        user: 0,
        system: 0,
        io: 0,
        irq: 0,
        sirq: 0
      }
    }
  },
  created () {
    this.get_disk_data()
  },
  methods: {
    get_disk_data: function () {
      var that = this
      this.$http.get('http://localhost:5001/smwsAPI/cpu_use_rate').then(function (response) {
        that.responseData = response.body
        that.flush_board_data()
        that.flush_chart_data()
        that.flush_card_data()
      })
    },
    to_format_time: function (t) {
      var h = ''
      var m = ''
      var s = ''
      if (t > 3600) {
        h = Math.floor(t / 3600)
        t -= h * 3600
        h += 'h'
      }
      if (t > 60) {
        m = Math.floor(t / 60)
        t -= m * 60
        m += 'm'
      }
      s = t + 's'
      return h + m + s
    },
    flush_board_data: function () {
      var option = {
        tooltip: {
          formatter: '{a}:{c}%'
        },
        series: [
          {
            name: '使用率',
            type: 'gauge',
            detail: {formatter: '{value}%'},
            data: [{value: 0, name: ''}],
            radius: '100%'
          }
        ]
      }
      var useRateData = this.responseData.data.use_rate.sort(function (a, b) {
        return b.timestamp - a.timestamp
      })
      option.series[0].data[0].value = useRateData[0].use_rate
      this.boardData = option
    },
    flush_chart_data: function () {
      var option = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: []
        },
        yAxis: {
          type: 'value',
          max: 100
        },
        series: [{
          data: [],
          type: 'line',
          areaStyle: {}
        }]
      }
      var useRateData = this.responseData.data.use_rate
      useRateData.sort(function (a, b) {
        return a.timestamp - b.timestamp
      }).forEach(element => {
        option.xAxis.data.push((new Date(element.timestamp * 1000).format('MM-dd h:m:s')))
        option.series[0].data.push(element.use_rate)
      })
      this.chartData = option
    },
    flush_card_data: function () {
      var useRateData = this.responseData.data.use_rate.sort(function (a, b) {
        return b.timestamp - a.timestamp
      })
      this.useTime = {
        user: this.to_format_time(useRateData[0].time.user),
        system: this.to_format_time(useRateData[0].time.system),
        io: this.to_format_time(useRateData[0].time.io),
        irq: this.to_format_time(useRateData[0].time.irq),
        sirq: this.to_format_time(useRateData[0].time.sirq)
      }
      this.count = useRateData[0].count
    }
  },
  watch: {
    selectMountPoint: function (val) {
      this.flush_board_data()
      this.flush_chart_data()
      this.flush_card_data()
    }
  }
}
</script>

<style lang="scss">
</style>
