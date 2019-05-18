<template>
    <div style="height: 100%;width: 100%;">
      <div style="height: 400px;width: 100%;">
          <div id="cpu-load-line-chart" style="height:100%;width:100%;"></div>
      </div>
      <div style="height: 200px;width;100%;margin-top:30px;">
        <div style="height: 100%;width: 23%;margin-left:2%;margin-right:2%;float:left;">
          <card title="LOAD_CURRENT%" :value="String(cardData.cur)"/>
        </div>
        <div style="height: 100%;width: 23%;margin-right:2%;float:left;">
          <card title="LOAD_AVG%" :value="String(cardData.avg)"/>
        </div>
        <div style="height: 100%;width: 22%;margin-right:2%;float:left;">
          <card title="LOAD_MAX%" :value="String(cardData.max)"/>
        </div>
        <div style="height: 100%;width: 22%;margin-right:2%;float:left;">
          <card title="LOAD_MIN%" :value="String(cardData.min)"/>
        </div>
      </div>
      <div style="height: 200px;width;100%;margin-top:30px;">
        <div style="height: 100%;width: 23%;margin-left:2%;margin-right:2%;float:left;">
          <card title="STATUS_USER%" :value="String(cardData.user)"/>
        </div>
        <div style="height: 100%;width: 23%;margin-right:2%;float:left;">
          <card title="STATUS_SYSTEM%" :value="String(cardData.system)"/>
        </div>
        <div style="height: 100%;width: 22%;margin-right:2%;float:left;">
          <card title="STATUS_IDLE%" :value="String(cardData.idle)"/>
        </div>
      </div>
    </div>
</template>

<script>
import echarts from 'echarts'
import card from '@/components/item/card'

export default {
  components: {
    card
  },
  mounted() {
    this.init()
  },
  data() {
    return {}
  },
  computed: {
    cpuData() {
      return this.$store.getters.cpuData
    },
    cardData() {
      var sum, max, min
      this.$store.getters.cpuData.forEach(record => {
        if (sum === undefined) {
          sum = record.used_rate
        } else {
          sum += record.used_rate
        }
        if (max === undefined || max < record.used_rate) {
          max = record.used_rate
        }
        if (min === undefined || min > record.used_rate) {
          min = record.used_rate
        }
      })
      var avg = (sum / this.$store.getters.cpuData.length).toFixed(2)
      return {
        avg: avg,
        max: max.toFixed(2),
        min: min.toFixed(2),
        cur: this.$store.getters.cpuData[this.$store.getters.cpuData.length - 1].used_rate.toFixed(2),
        user: this.$store.getters.cpuData[this.$store.getters.cpuData.length - 1].user_time_percent.toFixed(2),
        system: this.$store.getters.cpuData[this.$store.getters.cpuData.length - 1].system_time_percent.toFixed(2),
        idle: this.$store.getters.cpuData[this.$store.getters.cpuData.length - 1].idle_time_percent.toFixed(2)
      }
    }
  },
  watch: {
    cpuData() {
      this.updateView()
    }
  },
  methods: {
    init() {
      this.updateView()
    },
    updateView() {
      if (this.loadLinechart == undefined) {
        this.loadLinechart = echarts.init(document.getElementById('cpu-load-line-chart'))
        var option = JSON.parse(JSON.stringify(this.$conf.linechart_option))
        option.title = {
          text: 'CPU负载实时数据',
          right: 'center',
          textStyle: {
            fontSize: 30
          }
        }
        option.grid = {
          x: '2%',
          y: '10%',
          x2: '2%',
          y2: '5%'
        }
        this.loadLinechart.setOption(option)
        this.loadLinechart.showLoading();
      } else {
        var option = {
          xAxis: {
            data: []
          },
          yAxis: {
            max: 100,
            min: 0,
            name: 'CPU负载',
            type: 'value'
          },
          series: [
            {
              data: []
            }
          ]
        }
        this.$store.getters.cpuData.forEach(record => {
          if (record.time == 0) {
            option.xAxis.data.push('')
          } else {
            option.xAxis.data.push((new Date(record.timestamp * 1000)).toTimeString())
          }
          
          option.series[0].data.push(record.used_rate)
        });
        this.loadLinechart.setOption(option)
        this.loadLinechart.hideLoading()
      }
    }
  }
}
</script>

<style>
</style>