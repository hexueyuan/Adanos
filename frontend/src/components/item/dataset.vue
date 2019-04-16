<template>
    <div class="dataset">
        <div class="dataset-box">
            <div :id="datasetID" class="dataset-data"></div>
        </div>
    </div>
</template>

<script>
import echarts from 'echarts'
import uuidv1 from 'uuid/v1'

export default {
    props: {
        title: String,
        data: Array,
        base: String,
        start: String
    },
    data() {
        return {
            datasetID: "",
            options: {
                legend: {},
                tooltip: {
                    trigger: 'axis',
                    showContent: false
                },
                dataset: {
                    source: [
                        ['product', '2008', '2009', '2010', '2011', '2012', '2013'],
                        ['Matcha Latte', 41.1, 30.4, 65.1, 53.3, 83.8, 98.7],
                        ['Milk Tea', 86.5, 92.1, 85.7, 83.1, 73.4, 55.1],
                        ['Cheese Cocoa', 24.1, 67.2, 79.5, 86.4, 65.2, 82.5],
                        ['Walnut Brownie', 55.2, 67.1, 69.2, 72.4, 53.9, 39.1]
                    ]
                },
                xAxis: {type: 'category'},
                yAxis: {gridIndex: 0},
                grid: {top: '55%'},
                series: [
                    {type: 'line', smooth: true, seriesLayoutBy: 'row'},
                    {type: 'line', smooth: true, seriesLayoutBy: 'row'},
                    {type: 'line', smooth: true, seriesLayoutBy: 'row'},
                    {type: 'line', smooth: true, seriesLayoutBy: 'row'},
                    {
                        type: 'pie',
                        id: 'pie',
                        radius: '30%',
                        center: ['50%', '25%'],
                        label: {
                            formatter: '{b}: {@' + this.start + '} ({d}%)'
                        },
                        encode: {
                            itemName: this.base,
                            value: this.start,
                            tooltip: this.start
                        }
                    }
                ]
            }
        }
    },
    created() {
        this.datasetID = uuidv1()
    },
    mounted() {
        let datasetDom = document.getElementById(this.datasetID)
        this.dataset = echarts.init(datasetDom)

        this.dataset.on('updateAxisPointer', function (event) {
            var xAxisInfo = event.axesInfo[0]
            if (xAxisInfo) {
                var dimension = xAxisInfo.value + 1;
                myChart.setOption({
                    series: {
                        id: 'pie',
                        type: 'pie',
                        label: {
                            formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                        },
                        encode: {
                            value: dimension,
                            tooltip: dimension
                        }
                    }
                })
            }
        })

        this.dataset.setOption(this.options)
    },
    watch: {
        data: function(newVal) {
            console.log(JSON.stringify(this.options))
            this.options.dataset.source = newVal
            this.dataset.setOption(this.options)
            this.dataset.setOption({
                type: 'pie',
                id: 'pie',
                radius: '30%',
                center: ['50%', '25%'],
                label: {
                    formatter: '{b}: {@' + this.start + '} ({d}%)'
                },
                encode: {
                    itemName: this.base,
                    value: this.start,
                    tooltip: this.start
                }
             })
        }
    }
}
</script>

<style>
.dataset {
    height: 100%;
    width: 95%;
    margin: 0px auto;
}
.dataset-box {
    height: 100%;
    width: 100%;
    background-color: #f0f0f0;
    box-shadow: 0 5px 0 #e0e0e0;
    border-radius: 4px;
}
.dataset-data {
    height: 100%;
    width: 100%;
}
</style>
