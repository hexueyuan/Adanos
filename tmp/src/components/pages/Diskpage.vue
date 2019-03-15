<template>
    <el-row style="height:100%;">
        <!--el-col :span="24">
            <el-select v-model="selectMountPoint" placeholder="请选择挂载点">
                <el-option v-for="item in responseData.data.mount_points" :key="item" :value="item" :label="item" :selectMountPoint="item"></el-option>
            </el-select>
        </el-col-->
        <el-col :span="8" style="height:45vh;">
            <el-card style="height:100%">
            <Boardchart :chart-data="boardData" ></Boardchart>
            </el-card>
        </el-col>
        <el-col :span="8" style="height:45vh;">
            <el-card style="height:100%">
                <span style="width:100%; font-size:3vw">总容量</span><br/><br/>
                <span style="width:100%; color:green; font-size:6vw">{{ totalSpace }}</span><br/>
                <span style="width:100%; color:green; font-size:7vw">GB</span>
            </el-card>
        </el-col>
        <el-col :span="8" style="height:45vh;">
            <el-card style="height:100%">
                <span style="width:100%; font-size:3vw">剩余容量</span><br/><br/>
                <span style="width:100%; color:red; font-size:6vw">{{ restSpace }}</span><br/>
                <span style="width:100%; color:red; font-size:7vw">GB</span>
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
      selectMountPoint: '/',
      totalSpace: '',
      restSpace: ''
    }
  },
  created () {
    this.get_disk_data()
  },
  methods: {
    get_disk_data: function () {
      var that = this
      this.$http.get('http://localhost:5001/smwsAPI/disk_use_rate').then(function (response) {
        that.responseData = response.body
        that.flush_board_data()
        that.flush_chart_data()
        that.flush_card_data()
      })
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
      var useRateData = this.responseData.data.use_rate[this.selectMountPoint].sort(function (a, b) {
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
      var useRateData = this.responseData.data.use_rate[this.selectMountPoint]
      useRateData.sort(function (a, b) {
        return a.timestamp - b.timestamp
      }).forEach(element => {
        option.xAxis.data.push((new Date(element.timestamp * 1000).format('MM-dd h:m:s')))
        option.series[0].data.push(element.use_rate)
      })
      this.chartData = option
    },
    flush_card_data: function () {
      var useRateData = this.responseData.data.use_rate[this.selectMountPoint].sort(function (a, b) {
        return b.timestamp - a.timestamp
      })
      this.totalSpace = useRateData[0].total_space
      this.restSpace = (useRateData[0].total_space * (100 - useRateData[0].use_rate) / 100).toFixed(2)
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
