<template>
  <div>
    <div style="height: 500px;width: 100%;">
      <div id="disk-used-line-chart" style="height:100%;width:100%;"></div>
    </div>
    <div style="height: 210px;width;100%;margin-top:30px;">
      <div style="height: 100%;width: 23%;margin-left:2%;margin-right:2%;float:left;">
        <card title="USEDRATE_CURRENT%" :value="String(cardData.cur)"/>
      </div>
      <div style="height: 100%;width: 23%;margin-right:2%;float:left;">
        <card title="USEDRATE_AVG%" :value="String(cardData.avg)"/>
      </div>
      <div style="height: 100%;width: 22%;margin-right:2%;float:left;">
        <card title="USEDRATE_MAX%" :value="String(cardData.max)"/>
      </div>
      <div style="height: 100%;width: 22%;margin-right:2%;float:left;">
        <card title="USEDRATE_MIN%" :value="String(cardData.min)"/>
      </div>
    </div>
    <div style="height: 210px;width;100%;margin-top:30px;">
      <div style="height: 100%;width: 23%;margin-left:2%;margin-right:2%;float:left;">
        <card title="DISK_TOTAL(GB)" :value="String(cardData.total)"/>
      </div>
      <div style="height: 100%;width: 23%;margin-right:2%;float:left;">
        <card title="DISK_USED(GB)" :value="String(cardData.used)"/>
      </div>
      <div style="height: 100%;width: 22%;margin-right:2%;float:left;">
        <card title="DISK_FREE(GB)" :value="String(cardData.free)"/>
      </div>
    </div>
    <div style="height: 210px;width;100%;margin-top:30px;">
      <div style="height: 100%;width: 23%;margin-left:2%;margin-right:2%;float:left;">
        <card title="DISK_ACTIVE(GB)" :value="String(cardData.active)"/>
      </div>
      <div style="height: 100%;width: 23%;margin-right:2%;float:left;">
        <card title="DISK_INACTIVE(GB)" :value="String(cardData.inactive)"/>
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
    diskData() {
      return this.$store.getters.diskData
    },
    cardData() {
      var sum, max, min
      this.$store.getters.diskData.forEach(record => {
        if (sum === undefined) {
          sum = record.use_rate
        } else {
          sum += record.use_rate
        }
        if (max === undefined || max < record.use_rate) {
          max = record.use_rate
        }
        if (min === undefined || min > record.use_rate) {
          min = record.use_rate
        }
      })
      var avg = (sum / this.$store.getters.diskData.length).toFixed(2)
      return {
        avg: avg,
        max: max.toFixed(2),
        min: min.toFixed(2),
        cur: this.$store.getters.diskData[this.$store.getters.diskData.length - 1].use_rate.toFixed(2),
        total: this.$store.getters.diskData[this.$store.getters.diskData.length - 1].total.toFixed(2),
        used: this.$store.getters.diskData[this.$store.getters.diskData.length - 1].used.toFixed(2),
        free: this.$store.getters.diskData[this.$store.getters.diskData.length - 1].free.toFixed(2),
        active: this.$store.getters.diskData[this.$store.getters.diskData.length - 1].active.toFixed(2),
        inactive: this.$store.getters.diskData[this.$store.getters.diskData.length - 1].inactive.toFixed(2)
      }
    }
  },
  watch: {
    diskData() {
      this.updateView()
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
      }
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
        series: [
          {
            data: []
          }
        ]
      }
      this.$store.getters.diskData.forEach(record => {
        if (record.time == 0) {
          option.xAxis.data.push('')
        } else {
          option.xAxis.data.push((new Date(record.time * 1000)).toTimeString())
        }
        
        option.series[0].data.push(record.use_rate)
      });
      this.usedLinechart.setOption(option)
      this.usedLinechart.hideLoading()
    }
  }
}
</script>

<style lang="scss">
</style>
