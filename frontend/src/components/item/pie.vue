<template>
    <div class="pie">
        <div class="pie-box">
            <div :id="pieID" class="pie-data"></div>
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
        data: Array
    },
    data() {
        return {
            pieID: "",
            option: {
                baseOption: {
                    title : {
                        text: this.title,
                        subtext: this.subTitle,
                        x:'center',
                        textStyle: {
                            color: '#003366'
                        }
                    },
                    legend: {
                        data: []
                    },
                    series : [
                        {
                            type: 'pie',
                            data: this.series
                        }
                    ]
                },
                media: [
                    {
                        //水平布局
                        query: {
                            minAspectRatio: 1.5
                        },
                        option: {
                            legend: {
                                orient: 'vertical',
                                top: 'center',
                                right: '15%',
                            },
                            series: [
                                {
                                    radius : '60%',
                                    center: ['30%', '50%']
                                }
                            ]
                        }
                    },
                    {
                        //垂直布局
                        query: {
                            maxAspectRatio: 0.6
                        },
                        option: {
                            legend: {
                                orient: 'horizontal',
                                top: '10%',
                                right: 'center'
                            },
                            series: [
                                {
                                    radius : '60%',
                                    center: ['50%', '70%']
                                }
                            ]
                        }
                    },
                    {
                        //默认布局
                        query: {
                            minAspectRatio: 0.6,
                            maxAspectRatio: 1.5
                        },
                        option: {
                            legend: {
                                orient: 'vertical',
                                top: 10,
                                right: 10
                            },
                            series: [
                                {
                                    radius : '70%',
                                    center: ['50%', '50%']
                                }
                            ]
                        }
                    },
                    {
                        //PC全屏组件尺寸
                        query: {
                            minWidth: 1600
                        },
                        option: {
                            title: {
                                textStyle: {
                                    fontWeight: 1000,
                                    fontSize: 48
                                }
                            },
                            legend: {
                                textStyle: {
                                    fontSize: 32
                                },
                                itemWidth: 120,
                                itemHeight: 80
                            },
                            series: [
                                {
                                    label: {
                                        fontSize: 24
                                    }
                                }
                            ]
                        }
                    },
                    {
                        //PC半屏组件尺寸
                        query: {
                            minWidth: 600,
                            maxWidth: 1600
                        },
                        option: {
                            title: {
                                textStyle: {
                                    fontWeight: 1000,
                                    fontSize: 32
                                }
                            },
                            legend: {
                                textStyle: {
                                    fontSize: 24
                                },
                                itemWidth: 50,
                                itemHeight: 20
                            },
                            series: [
                                {
                                    label: {
                                        fontSize: 18
                                    }
                                }
                            ]
                        }
                    },
                    {
                        //PC四分之一屏组件尺寸
                        query: {
                            maxWidth: 600
                        },
                        option: {
                            title: {
                                textStyle: {
                                    fontWeight: 1000,
                                    fontSize: 18
                                }
                            },
                            legend: {
                                textStyle: {
                                    fontSize: 14
                                },
                                itemWidth: 20,
                                itemHeight: 8
                            },
                            series: [
                                {
                                    label: {
                                        fontSize: 12
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
    },
    created() {
        this.pieID = uuidv1()
    },
    mounted() {
        this.flush_pie_chart()
    },
    methods: {
        flush_pie_chart: function() {
            var legend = []
            this.data.forEach(element => {
                legend.push(element.name)
            });
            this.option.baseOption.legend.data = legend
            this.option.baseOption.series[0].data = this.data
            if (!this.pieChart) {
                this.pieChart = echarts.init(document.getElementById(this.pieID))
            }
            this.pieChart.setOption(this.option)
        }
    },
    watch: {
        data: function() {
            this.flush_pie_chart()
        }
    }
}
</script>

<style>
.pie {
    height: 100%;
    width: 100%;
}
.pie-box {
    height: 100%;
    width: 100%;
    margin: 0px auto;
}
.pie-data {
    height: 100%;
    width: 100%;
}
</style>
