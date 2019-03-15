<template>
  <div v-show="!isEmpty" :id="elID"></div>
</template>

<script>
import echarts from 'echarts'
import uuidv1 from 'uuid/v1'

export default {
  name: 'echarts',
  props: {
    chartData: Object
  },
  data () {
    return {
      elID: '',
      chart: null,
      isEmpty: true
    }
  },
  created () {
    this.elID = uuidv1()
  },
  mounted () {
    let echartsDOM = document.getElementById(this.elID)
    echartsDOM.style.width = window.innerWidth * 0.75 / 3 - 10 + 'px'
    echartsDOM.style.height = window.innerHeight * 0.95 * 0.5 + 'px'

    let myEcharts = echarts.init(echartsDOM)
    this.chart = myEcharts
    this.chartData.grid = {
      x: 0,
      y: 0,
      x2: 0,
      y2: 0
    }
    myEcharts.setOption(this.chartData)
  },
  watch: {
    chartData: {
      handler (newVal) {
        this.isEmpty = false
        if (this.chart) {
          this.chart.setOption(newVal)
        }
      }
    }
  }
}
</script>

<style lang="scss">
</style>
