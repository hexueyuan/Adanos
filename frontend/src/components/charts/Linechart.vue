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
    echartsDOM.style.width = window.innerWidth * 0.82 + 'px'
    echartsDOM.style.height = window.innerHeight * 0.45 + 'px'

    let myEcharts = echarts.init(echartsDOM)
    this.chart = myEcharts
    this.chartData.grid = {
      x: '2%',
      y: '2%',
      x2: '2%',
      y2: '5%'
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
