<template>
    <div class="linechart">
        <div class="linechart-box">
            <div :id="chartID" class="linechart-data"></div>
        </div>
    </div>
</template>

<script>
import echarts from 'echarts'
import uuidv1 from 'uuid/v1'

export default {
    props: {
        title: String,
        data: Object
    },
    componenst: {
        echarts
    },
    data() {
        return {
            chartID: "",
            option: {
                baseOption: {
                    title: {
                        text: this.title,
                        right: 'center'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: []
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [
                        {
                            data: [],
                            type: 'line',
                            smooth: true,
                            areaStyle: {
                                color: '#CAE1FF'
                            },
                            lineStyle: {
                                color: '#CAE1FF'
                            }
                        }
                    ],
                    grid: {
                        x: '5%',
                        y: '15%',
                        x2: '5%',
                        y2: '8%'
                    }
                },
                media: [
                    {
                        //PC全屏
                        query: {
                            minWidth: 1600
                        },
                        option: {
                            title: {
                                textStyle: {
                                    fontSize: 32
                                }
                            }
                        }
                    },
                    {
                        //PC半屏
                        query: {
                            minWidth: 600,
                            maxWidth: 1600
                        },
                        option: {
                            title: {
                                textStyle: {
                                    fontSize: 32
                                }
                            }
                        }
                    },
                    {
                        //PC小屏
                        query: {
                            maxWidth: 600
                        },
                        option: {
                            title: {
                                textStyle: {
                                    fontSize: 24
                                }
                            }
                        }
                    }
                ]
            }
        }
    },
    created () {
        this.chartID = uuidv1()
    },
    watch: {
        data: function(newValue) {
            this.flush_data(newValue)
            this.create_chart()
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
            this.linechart.setOption(this.option)
        },
        flush_data: function(newValue) {
            var lenX = newValue.xAxis?newValue.xAxis.length:0
            var lenY = newValue.yAxis?newValue.yAxis.length:0
            if (lenX === lenY && lenX !== 0) {
                this.option.baseOption.xAxis.data = newValue.xAxis
                this.option.baseOption.series[0].data = newValue.yAxis
            } else if (lenX !== 0 && lenY !== 0) {
                //如果x和y长度不相等
                //求最小长度，舍弃掉超长部分
                var len = lenX>lenY?lenY:lenX
                this.option.baseOption.xAxis.data = newValue.xAxis.splice(0, len)
                this.option.baseOption.series[0].data = newValue.yAxis.splice(0, len)
            }
        }
    }
}
</script>

<style>
.linechart {
    height: 100%;
    width: 100%;
}
.linechart-box {
    height: 100%;
    width: 100%;
    margin: 0px auto;
}
.linechart-data {
    height: 100%
}
</style>
