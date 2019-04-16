<template>
  <div class="dashboard">
    <div class="dashboard-box">
        <div :id="dashboardID" class="dashboard-data"></div>
    </div>
  </div>
</template>

<script>
import echarts from 'echarts'
import uuidv1 from 'uuid/v1'

export default {
    props: {
        value: String,
        name: String
    },
    data() {
        return {
            dashboardID: "",
            option: {
                baseOption: {
                    backgroundColor: 'white',
                    title: {
                        text: this.name,
                        subtext: this.name,
                        x:'center',
                        bottom: '30%',
                        textStyle: {
                            fontWeight: 'bold',
                            color: '#0095ff'
                        },
                        subtextStyle: {
                            fontWeight: 'normal',
                            fontSize: 20,
                            color: "#0095ff"
                        }
                    },
                    tooltip: {
                        formatter: "{a} <br/>{c}%"
                    },
                    series: [
                        {
                            splitNumber: 10,
                            name: '指标',
                            type: 'gauge',
                            radius : '95%',
                            data: [{value: 0}],
                            axisLine: {
                                show: false,
                                lineStyle: {
                                    width: 10,
                                    shadowBlur: 0,
                                    color: [
                                        [1, 'white']
                                    ]
                                }
                            },
                            splitLine: {
                                length: 30,
                                lineStyle: {
                                    color: "black"
                                }
                            },
                            axisLabel: {
                                show: false
                            },
                            pointer: {
                                show: false
                            },
                            detail: {
                                show: false
                            }
                        },
                        {
                            splitNumber: 50,
                            type: 'gauge',
                            radius: '91%',
                            data: [{value: 0}],
                            axisLine: {
                                lineStyle: {
                                    color: [[1, '#0095ff']],
                                    width: 10
                                }
                            },
                            splitLine: {
                                length: 10,
                                lineStyle: {
                                    color: 'white',
                                    width: 4
                                }
                            },
                            axisTick: {
                                show: false
                            },
                            axisLabel: {
                                show: false
                            },
                            pointer: {
                                show: false
                            },
                            detail: {
                                show: false
                            }
                        },
                        {
                            splitNumber: 1,
                            type: 'gauge',
                            radius: '85%',
                            data: [{value: 0}],
                            axisLine: {
                                lineStyle: {
                                    color: [[1, '#0095ff']],
                                    width: 2
                                }
                            },
                            splitLine: {
                                length: 10,
                                lineStyle: {
                                    color: 'white',
                                    width: 4
                                }
                            },
                            axisTick: {
                                show: false
                            },
                            axisLabel: {
                                show: false
                            },
                            pointer: {
                                show: false
                            },
                            detail: {
                                show: false
                            }
                        },
                        {
                            splitNumber: 20,
                            type: 'gauge',
                            radius: '81%',
                            data: [{value: 0}],
                            axisLine: {
                                lineStyle: {
                                    color: [[0, '#ff0090'], [1, '#ff6600']],
                                    width: 25
                                }
                            },
                            splitLine: {
                                length: 25,
                                lineStyle: {
                                    color: 'white',
                                    width: 8
                                }
                            },
                            axisTick: {
                                show: false
                            },
                            axisLabel: {
                                show: false
                            },
                            pointer: {
                                show: false
                            },
                            detail: {
                                show: false
                            }
                        },
                        {
                            splitNumber: 1,
                            type: 'gauge',
                            radius: '70%',
                            data: [{value: 0}],
                            axisLine: {
                                lineStyle: {
                                    color: [[1, '#0095ff']],
                                    width: 2
                                }
                            },
                            splitLine: {
                                show: false
                            },
                            axisLabel: {
                                show: false
                            },
                            pointer: {
                                show: false
                            },
                            detail: {
                                show: false
                            }
                        },
                        {
                            name: this.name,
                            splitNumber: 20,
                            type: 'gauge',
                            radius: '68%',
                            data: [{value: this.value}],
                            axisLine: {
                                lineStyle: {
                                    color: [[0, '#fcff00'], [1, '##FF7F24']],
                                    width: 20
                                }
                            },
                            splitLine: {
                                length: 20,
                                lineStyle: {
                                    color: 'white',
                                    width: 6
                                }
                            },
                            axisTick: {
                                show: false
                            },
                            axisLabel: {
                                show: false
                            },
                            detail: {
                                show: false
                            },
                            pointer: {
                                width: 10
                            },
                            itemStyle: {
                                color: 'black'
                            }
                        }
                    ],
                    grid: {
                        width: '100%',
                        height: '100%',
                        left: '0%',
                        right: '0%',
                        bottom: '25%'
                    }
                },
                media: [
                    {
                        query: {
                            minWidth: 1600
                        },
                        option: {
                            title: {
                                textStyle: {
                                    fontSize: 48
                                }
                            }
                        }
                    },
                    {
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
        this.dashboardID = uuidv1()
    },
    methods: {
        flush_value: function() {
            this.option.baseOption.series[5].data[0].value = this.value
            if (!this.dashboard) {
                let echartsDOM = document.getElementById(this.dashboardID)
                this.dashboard = echarts.init(echartsDOM)
            }
            this.dashboard.setOption(this.option)
        }
    },
    watch: {
        value: function() {
            this.flush_value()
        }
    }
}
</script>

<style>
.dashboard {
    height: 100%;
    width: 100%;
}
.dashboard-box {
    height: 100%;
    width: 100%;
    margin: 0px auto;
}
.dashboard-data {
    height: 100%;
    width: 100%;
}
</style>
