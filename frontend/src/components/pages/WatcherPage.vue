<template>
    <div style="height: 100%;">
        <el-row class="watcherPage-select-container">
            <el-radio-group v-model="radio" class="watcherPage-select-main">
                <el-radio-button label="实时"></el-radio-button>
                <el-radio-button label="近24小时"></el-radio-button>
                <el-radio-button label="近7天"></el-radio-button>
                <el-radio-button label="选择时间"></el-radio-button>
            </el-radio-group>
            <div class="watcherpage-time-picker" v-if="manual">
                <el-date-picker
                    v-model="time"
                    type="datetimerange"
                    range-separator="至"
                    start-placeholder="开始时间"
                    end-placeholder="结束时间">
                </el-date-picker>
            </div>
        </el-row>
        <hr>
        <div class="watcher-chart" style="height: 40%;width: 100%">

        </div>
        <div class="watcher-data-items"></div>
    </div>
</template>

<script>
import linechart from '@/components/item/linechart'

export default {
    components: {
        linechart
    },
    created() {
        this.get_mock_data()
    },
    mounted() {
        if (this.timer) {
            clearInterval(this.timer)
        } else {
            this.timer = setInterval(() => {
                this.get_mock_data()
            }, 10000)
        }
    },
    data() {
        return {
            radio: '实时',
            time: [new Date(), new Date()],
            manual: false,
            requestData: [],
            chartData: {
                tooltip: {
                    trigger: 'axis'
                },
                xAxis: {
                    data: [],
                    type: 'category',
                    boundaryGap: false
                },
                yAxis: {
                    type: 'value'
                },
                series: [{
                    data: [],
                    type: 'line',
                    areaStyle: {}
                }]
            }
        }
    },
    watch: {
        radio: function(val) {
            if (val == "选择时间") {
                this.manual = true
            } else {
                this.manual = false
            }
        }
    },
    methods: {
        get_mock_data: function () {
            var that = this
            this.$http.get('http://localhost:5001/smwsAPI/mock_data').then(function (response) {
                if (response.body.status == "OK") {
                    that.flush_chart_data(response.body.data)
                }
            })
        },
        flush_chart_data: function(val) {
            var option = this.chartData
            option.xAxis.data = []
            option.series[0].data = []
            val.sort(function (a, b) {
                return a.time_stamp > b.time_stamp
            }).forEach(element => {
                option.xAxis.data.push(element.time_stamp)
                option.series[0].data.push(element.value)
            });
            this.chartData = option
            console.log("flush")
        }
    },
    distroyed() {
        clearInterval(this.timer)
    }
}
</script>

<style>
.watcherPage-select-container {
    margin: 5px;
}
.watcherPage-select-main {
    float: left;
}
.watcherPage-time-picker {
    float: left;
}
.watcher-chart {
    height: 100%;
}
</style>
