<template>
    <div :id="elID"></div>
</template>

<script>
import echarts from 'echarts'
import uuidv1 from 'uuid/v1'

export default {
    props: {
        chartData: Object
    },
    data () {
        return {
            elID: ''
        }
    },
    created () {
        this.elID = uuidv1()
    },
    mounted () {
        var myChart = echarts.init(document.getElementById(this.elID))
        myChart.setOption(this.chartData)
    }
}
</script>