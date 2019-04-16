<template>
    <div style="height: 100%;width: 100%;">
      <div style="height: 30%;width: 100%;">
          <linechart title="CPU负载情况" :data="load_data"/>
      </div>
      <div style="height: 10%;width;100%;">
        <div style="height: 100%;width: 22%;margin-left:5%;margin-right:1%;float:left;">
          <card title="当前负载" value="0.86"/>
        </div>
        <div style="height: 100%;width: 22%;margin-right:1%;float:left;">
          <card title="平均负载" value="0.52" type="common" />
        </div>
        <div style="height: 100%;width: 22%;margin-right:1%;float:left;">
          <card title="最大负载" value="0.96" type="good" />
        </div>
        <div style="height: 100%;width: 22%;margin-right:1%;float:left;">
          <card title="最小负载" value="0.06" type="bad" />
        </div>
      </div>
      <div style="height: 80%;width:90%;margin:10px auto;">
        <el-table :data=this.proccess_data style="width:100%">
          <el-table-column prop="cpu" label="CPU%" width="180"/>
          <el-table-column prop="mem" label="内存%" width="180"/>
          <el-table-column prop="pid" label="PID" width="180"/>
          <el-table-column prop="user" label="用户" width="180"/>
          <el-table-column prop="time" label="运行时间" width="180"/>
          <el-table-column prop="name" label="进程名"/>
        </el-table>
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
      card
    },
    mounted() {
      this.request_data()
      if (this.timer) {
          clearInterval(this.timer)
      } else {
          this.timer = setInterval(() => {
              this.update_data()
          }, 10000)
      }
    },
    data() {
      return {
        responseData: {},
        time_radio: '24小时',
        load_data: {
          xAxis: [],
          yAxis: []
        },
        proccess_data: []
      }
    },
    watch: {
    },
    methods: {
      request_data: function () {
        var that = this
        this.$http.post('http://localhost:5001/smwsAPI/cpu_info', {}).then(function (response) {
          if (response.body.status == "success") {
            that.responseData = response.body.data
          }
        })
      },
      //更新负载折线图数据
      update_load_data: function() {
        var data = this.responseData.load
        var tmp_data = {
          xAxis: [],
          yAxis: []
        }
        data.forEach(element => {
          tmp_data.xAxis.push((new Date(element.time * 1000)).toLocaleString())
          tmp_data.yAxis.push(element.value)
        })
        this.load_data = tmp_data
      },
      update_proccess_data: function() {
        this.proccess_data = this.responseData.top20
      },
      update_data: function () {
        this.request_data()
        this.update_load_data()
        this.update_proccess_data()
      }
    },
    distroyed() {
        clearInterval(this.timer)
    }
}
</script>

<style>
</style>
