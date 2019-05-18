<template>
  <div style="height: 100%">
    <div style="height: 400px;width: 100%;">
      <div id="memory-used-line-chart" style="height:100%;width:100%;"></div>
    </div>
    <div style="height: 200px;width;100%;margin-top:30px;">
      <div style="height: 100%;width: 23%;margin-left:2%;margin-right:2%;float:left;">
        <card title="MEM_USEDRATE_CURRENT%" :value="String(cardData.mem_cur)"/>
      </div>
      <div style="height: 100%;width: 23%;margin-right:2%;float:left;">
        <card title="MEM_USEDRATE_AVG%" :value="String(cardData.mem_avg)"/>
      </div>
      <div style="height: 100%;width: 22%;margin-right:2%;float:left;">
        <card title="MEM_USEDRATE_MAX%" :value="String(cardData.mem_max)"/>
      </div>
      <div style="height: 100%;width: 22%;margin-right:2%;float:left;">
        <card title="MEM_USEDRATE_MIN%" :value="String(cardData.mem_min)"/>
      </div>
    </div>
    <div style="height: 200px;width;100%;margin-top:30px;">
      <div style="height: 100%;width: 23%;margin-left:2%;margin-right:2%;float:left;">
        <card title="MEM_TOTAL(GB)" :value="String(cardData.mem_total)"/>
      </div>
      <div style="height: 100%;width: 23%;margin-right:2%;float:left;">
        <card title="MEM_USED(GB)" :value="String(cardData.mem_used)"/>
      </div>
      <div style="height: 100%;width: 22%;margin-right:2%;float:left;">
        <card title="MEM_FREE(GB)" :value="String(cardData.mem_free)"/>
      </div>
    </div>
    <div style="height: 200px;width;100%;margin-top:30px;">
      <div style="height: 100%;width: 23%;margin-left:2%;margin-right:2%;float:left;">
        <card title="SWAP_USEDRATE_CURRENT%" :value="String(cardData.swap_cur)"/>
      </div>
      <div style="height: 100%;width: 23%;margin-right:2%;float:left;">
        <card title="SWAP_USEDRATE_AVG%" :value="String(cardData.swap_avg)"/>
      </div>
      <div style="height: 100%;width: 22%;margin-right:2%;float:left;">
        <card title="SWAP_USEDRATE_MAX%" :value="String(cardData.swap_max)"/>
      </div>
      <div style="height: 100%;width: 22%;margin-right:2%;float:left;">
        <card title="SWAP_USEDRATE_MIN%" :value="String(cardData.swap_min)"/>
      </div>
    </div>
    <div style="height: 200px;width;100%;margin-top:30px;">
      <div style="height: 100%;width: 23%;margin-left:2%;margin-right:2%;float:left;">
        <card title="SWAP_TOTAL(GB)" :value="String(cardData.swap_total)"/>
      </div>
      <div style="height: 100%;width: 23%;margin-right:2%;float:left;">
        <card title="SWAP_USED(GB)" :value="String(cardData.swap_used)"/>
      </div>
      <div style="height: 100%;width: 22%;margin-right:2%;margin-bottom:30px;float:left;">
        <card title="SWAP_FREE(GB)" :value="String(cardData.swap_free)"/>
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
    memoryData() {
      return this.$store.getters.memoryData
    },
    cardData() {
      var mem_sum, mem_max, mem_min, swap_sum, swap_max, swap_min
      this.$store.getters.memoryData.forEach(record => {
        if (mem_sum === undefined) {
          mem_sum = record.mem_used_rate
        } else {
          mem_sum += record.mem_used_rate
        }
        if (swap_sum === undefined) {
          swap_sum = record.swap_used_rate
        } else {
          swap_sum += record.swap_used_rate
        }
        if (mem_max === undefined || mem_max < record.mem_used_rate) {
          mem_max = record.mem_used_rate
        }
        if (mem_min === undefined || mem_min > record.mem_used_rate) {
          mem_min = record.mem_used_rate
        }
        if (swap_max === undefined || swap_max < record.swap_used_rate) {
          swap_max = record.swap_used_rate
        }
        if (swap_min === undefined || swap_min > record.swap_used_rate) {
          swap_min = record.swap_used_rate
        }
      })
      var mem_avg = (mem_sum / this.$store.getters.memoryData.length).toFixed(2)
      var swap_avg = (swap_sum / this.$store.getters.memoryData.length).toFixed(2)
      return {
        mem_avg: mem_avg,
        mem_max: mem_max,
        mem_min: mem_min,
        mem_cur: this.$store.getters.memoryData[this.$store.getters.memoryData.length - 1].mem_used_rate,
        mem_total: this.$store.getters.memoryData[this.$store.getters.memoryData.length - 1].mem_total,
        mem_used: this.$store.getters.memoryData[this.$store.getters.memoryData.length - 1].mem_used,
        mem_free: this.$store.getters.memoryData[this.$store.getters.memoryData.length - 1].mem_free,
        swap_avg: swap_avg,
        swap_max: swap_max,
        swap_min: swap_min,
        swap_cur: this.$store.getters.memoryData[this.$store.getters.memoryData.length - 1].swap_used_rate,
        swap_total: this.$store.getters.memoryData[this.$store.getters.memoryData.length - 1].swap_total,
        swap_used: this.$store.getters.memoryData[this.$store.getters.memoryData.length - 1].swap_used,
        swap_free: this.$store.getters.memoryData[this.$store.getters.memoryData.length - 1].swap_free
      }
    }
  },
  watch: {
    memoryData() {
      this.updateView()
    }
  },
  methods: {
    init() {
      this.updateView()
    },
    updateView() {
      if (this.usedLinechart == undefined) {
        this.usedLinechart = echarts.init(document.getElementById('memory-used-line-chart'))
        var initOption = JSON.parse(JSON.stringify(this.$conf.linechart_option))
        initOption.title = {
          text: '内存使用率实时数据',
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
            name: '内存',
            type: 'line',
            data: []
          },
          {
            name: '交换区',
            type: 'line',
            data: [],
            smooth: true,
            areaStyle: {
                color: '#E4B2B5'
            },
            lineStyle: {
                color: '#E4B2B5'
            }
          }
        ]
      }
      this.$store.getters.memoryData.forEach(record => {
        if (record.time == 0) {
          option.xAxis.data.push('')
        } else {
          option.xAxis.data.push((new Date(record.timestamp * 1000)).toTimeString())
        }
        
        option.series[0].data.push(record.mem_used_rate)
        option.series[1].data.push(record.swap_used_rate)
      });
      this.usedLinechart.setOption(option)
      this.usedLinechart.hideLoading()
    }
  }
}
</script>

<style lang="scss">
</style>
