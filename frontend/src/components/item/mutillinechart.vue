<template>
    <div class="mutillinechart">
        <div class="mutillinechart-box">
            <div :id="chartID" class="mutillinechart-data"></div>
        </div>
    </div>
</template>

<script>
import echarts from 'echarts'
import uuidv1 from 'uuid/v1'

export default {
    props: {
        title: String,
        subTitle: String,
        legend: Array,
        data: Array
    },
    componenst: {
        echarts
    },
    data() {
        return {
            chartID: "",
            option: {
                title: {
                    text: this.title,
                    subtext: this.subTitle,
                    x: 'left'
                },
                legend: {},
                xAxis: {type: 'category'},
                yAxis: {gridIndex: 0},
                series: [],
                dataset: {
                    source: []
                },
                grid: {
                        x: '5%',
                        y: '15%',
                        x2: '5%',
                        y2: '8%'
                    }
            }
        }
    },
    created () {
        this.chartID = uuidv1()
    },
    watch: {
        data: function() {
            this.flush_chart()
        }
    },
    methods: {
        //根据数据创建折线图
        create_chart: function() {
            if (!this.linechart) {
                var echartsDOM = document.getElementById(this.chartID)
                echartsDOM.style.width = "100%"
                echartsDOM.style.height = "100%"

                this.linechart = echarts.init(echartsDOM)
            }
        },
        flush_chart: function(newValue) {
            this.option.series = []
            this.option.dataset.source = [this.legend]
            for (var index = 0; index < this.data.length; index++) {
                this.option.dataset.source.push(this.data[index])
                this.option.series.push({type: 'line', smooth: true, seriesLayoutBy: 'row'})
            }
            if (!this.linechart) {
                this.create_chart()
            }
            this.linechart.setOption(this.option)
        }
    }
}
</script>

<style>
.mutillinechart {
    height: 100%;
    width: 100%;
}
.mutillinechart-box {
    height: 100%;
    margin: 0px auto;
}
.mutillinechart-data {
    height: 100%
}
</style>
