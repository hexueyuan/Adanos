<template>
  <div style="height: 100%">

    <div style="height: 100%;width: 24.5%;float: left;margin-left:0;margin-right:0.5%;margin-bottom:20px;">
      <div style="height: 49%;width: 100%;margin-bottom:2%;">
        <dashboard name="内存当前使用情况" :value="this.memoryCurrentUseRate"/>
      </div>
      <div style="height: 49%;width: 100%;">
        <dashboard name="内存交换区当前使用请况" :value="this.swapCurrentUseRate"/>
      </div>
    </div>

    <div style="height: 100%;width: 75%;float: left;">

      <div style="height: 49%;width: 100%;margin-bottom: 1%">
        <div style="width: 100%;height: 15%;margin-bottom: 1%;float:left;">
          <div style="width: 49%;float: left;margin-left:0;margin-right:1%">
            <card title="内存总量(MB)" :value="this.memoryTotal" type="good"/>
          </div>
          <div style="width: 50%;float: left;margin-left:0;margin-right:0;">
            <card title="内存剩余量(MB)" :value="this.memoryRest" type="warning"/>
          </div>
        </div>

        <div style="width:100%;height: 84%;float:left">
          <el-row class="CPUPage-select-container" style="float: left;width:100%;height:8%;margin-bottom:10px;">
            <el-radio-group v-model="radio" class="CPUPage-select-main">
              <el-radio-button label="实时"></el-radio-button>
              <el-radio-button label="近24小时"></el-radio-button>
              <el-radio-button label="近7天"></el-radio-button>
              <el-radio-button label="选择时间"></el-radio-button>
            </el-radio-group>
            <div class="CPUPage-time-picker" v-if="manual">
              <el-date-picker
                  v-model="time"
                  type="datetimerange"
                  range-separator="至"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间">
              </el-date-picker>
            </div>
          </el-row>
          <hr class="float: left;width:100%;height:2%;">
          <div style="width: 100%;height:87%;float:left;">
            <linechart title="内存使用情况" :data="this.memorySelectTimeslotUseRate"/>
          </div>
        </div>
      </div>
      <div style="height: 49%;width: 100%;">
        <div style="width: 100%;height: 15%;margin-bottom: 1%;float:left;">
          <div style="width: 49%;float: left;margin-left:0;margin-right:1%">
            <card title="内存交换区总量(MB)" :value="this.swapTotal" type="good"/>
          </div>
          <div style="width: 50%;float: left;margin-left:0;margin-right:0;">
            <card title="内存交换区剩余量(MB)" :value="this.swapRest" type="warning"/>
          </div>
        </div>

        <div style="width:100%;height: 84%;float:left">
          <el-row class="CPUPage-select-container" style="float: left;width:100%;height:8%;margin-bottom:10px;">
            <el-radio-group v-model="radio" class="CPUPage-select-main">
              <el-radio-button label="实时"></el-radio-button>
              <el-radio-button label="近24小时"></el-radio-button>
              <el-radio-button label="近7天"></el-radio-button>
              <el-radio-button label="选择时间"></el-radio-button>
            </el-radio-group>
            <div class="CPUPage-time-picker" v-if="manual">
              <el-date-picker
                  v-model="time"
                  type="datetimerange"
                  range-separator="至"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间">
              </el-date-picker>
            </div>
          </el-row>
          <hr class="float: left;width:100%;height:3%;">
          <div style="width: 100%;height:87%;float:left;">
            <linechart title="内存交换区使用情况" :data="this.swapSelectTimeslotUseRate"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import linechart from '@/components/item/linechart'
import card from '@/components/item/card'
import pie from '@/components/item/pie'
import dashboard from '@/components/item/dashboard'
import mutillinechart from '@/components/item/mutillinechart'

export default {
    components: {
        linechart,
        card,
        pie,
        dashboard,
        mutillinechart
    },
    mounted() {
      this.request_data()
      if (this.timer) {
          clearInterval(this.timer)
      } else {
          this.timer = setInterval(() => {
              this.request_data()
          }, 10000)
      }
    },
    data() {
        return {
            radio: '实时',
            time: [new Date(), new Date()],
            manual: false,
            //服务器返回数据
            responseData: {},
            memoryCurrentUseRate: '0',
            swapCurrentUseRate: '0',
            memoryTotal: '0',
            swapTotal: '0',
            memoryRest: '0',
            swapRest: '0',
            memorySelectTimeslotUseRate: {
              xAxis: [],
              yAxis: []
            },
            swapSelectTimeslotUseRate: {
              xAxis: [],
              yAxis: []
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
        request_data: function () {
            var that = this
            this.$http.post('http://localhost:5001/smwsAPI/memory_info', {}).then(function (response) {
                if (response.body.status == "success") {
                    that.responseData = response.body.data
                }
            })
        },
        flush_page: function () {
          this.memoryTotal = this.responseData.memory.total.toString()
          this.memoryRest = this.responseData.memory.rest.toString()
          this.swapTotal = this.responseData.swap.total.toString()
          this.swapRest = this.responseData.swap.rest.toString()
          this.memoryCurrentUseRate = (this.responseData.memory.currentUseRate * 100).toFixed(2)
          this.swapCurrentUseRate = (this.responseData.swap.currentUseRate * 100).toFixed(2)
          var memoryUseRateXAxis = []
          var memoryUserateYAxis = []
          this.responseData.memory.selectTimeslotUseRate.forEach(item => {
            memoryUseRateXAxis.push((new Date(item.time)).toLocaleString())
            memoryUserateYAxis.push(item.value)
          })
          var swapUseRateXAxis = []
          var swapUserateYAxis = []
          this.responseData.swap.selectTimeslotUseRate.forEach(item => {
            swapUseRateXAxis.push((new Date(item.time)).toLocaleString())
            swapUserateYAxis.push(item.value)
          })
          this.memorySelectTimeslotUseRate = {
            xAxis: memoryUseRateXAxis,
            yAxis: memoryUserateYAxis
          }
          this.swapSelectTimeslotUseRate = {
            xAxis: swapUseRateXAxis,
            yAxis: swapUserateYAxis
          }
        }
    },
    watch: {
      responseData: function() {
        this.flush_page()
      }
    },
    distroyed() {
        clearInterval(this.timer)
    }
}
</script>

<style lang="scss">
</style>
