<template>
    <div style="width: 100%;height: 100%;">
        <div style="float: left;height: 65%; width: 100%;margin-top:10px;margin-bottom: 10px;">
            <div class="l-half-box">
                <dashboard :value="dashboardVal" name="使用率"/>
            </div>
            <div class="r-half-box">
                <div class="lt-quarter-box">
                    <dashboard :value="dashboardVal" name="留存率"/>
                </div>
                <div class="rt-quarter-box">
                    <dashboard :value="dashboardVal" name="死亡率"/>
                </div>
                <div class="lb-quarter-box">
                    <dashboard :value="dashboardVal" name="出生率"/>
                </div>
                <div class="rb-quarter-box">
                    <dashboard :value="dashboardVal" name="使用率"/>
                </div>
            </div>
        </div>
        <div style="float: left; width: 100%;">
            <div id="card-good" style="margin-top: 10px;width: 50%;float: left;margin-right:1%;">
                <card title="使用率" :value="cardMsg" type="good"/>
            </div>
            <div id="card-warning" style="margin-top: 10px;width: 49%;float: left;">
                <card title="留存率" :value="cardMsg" type="warning"/>
            </div>
            <div id="card-bad" style="margin-top: 10px;width: 50%;float: left;margin-right:1%;">
                <card title="死亡率" :value="cardMsg" type="bad"/>
            </div>
            <div id="card-common" style="margin-top: 10px;width: 49%;float: left;">
                <card title="出生率" :value="cardMsg" type="common"/>
            </div>
        </div>
        <div style="float: left; width: 30%; display: inline-block;">
            <div id="card-good" style="margin-top: 20px;">
                <card title="使用率" :value="cardMsg" type="good"/>
            </div>
            <div id="card-warning" style="margin-top: 10px;">
                <card title="留存率" :value="cardMsg" type="warning"/>
            </div>
            <div id="card-bad" style="margin-top: 10px;">
                <card title="死亡率" :value="cardMsg" type="bad"/>
            </div>
            <div id="card-common" style="margin-top: 10px;">
                <card title="出生率" :value="cardMsg" type="common"/>
            </div>
        </div>
        <div style="float: left;width: 69%;margin-left:1%;">
            <div id="line-chart1" style="margin-top: 20px;display: inline-block;width: 100%;">
                <linechart title="使用情况" :data="linechartData"/>
            </div>
        </div>
        <div style="float: left;width: 100%;margin-bottom: 10px;margin-top: 10px;">
            <linechart title="浪费情况" :data="linechartData"/>
        </div>
        <div style="float: left;height: 80%; width: 100%;margin-top: 10px; margin-bottom: 10px;">
            <pie title="product sales" sub-title="last year" :legend="['product1', 'product2', 'product3', 'product4', 'product5']" :series="this.pieData" item-name="sales"/>
        </div>
        <div style="float: left;height: 80%;width: 100%;margin-top: 10px;margin-bottom: 10px;">
            <div class="l-half-box">
                <pie title="product sales" sub-title="last year" :legend="['product1', 'product2', 'product3', 'product4', 'product5']" :series="this.pieData" item-name="sales"/>
            </div>
            <div class="r-half-box">
                <div class="lt-quarter-box">
                    <pie title="product sales" sub-title="last year" :legend="['product1', 'product2', 'product3', 'product4', 'product5']" :series="this.pieData" item-name="sales"/>
                </div>
                <div class="rt-quarter-box">
                    <pie title="product sales" sub-title="last year" :legend="['product1', 'product2', 'product3', 'product4', 'product5']" :series="this.pieData" item-name="sales"/>
                </div>
                <div class="lb-quarter-box">
                    <pie title="product sales" sub-title="last year" :legend="['product1', 'product2', 'product3', 'product4', 'product5']" :series="this.pieData" item-name="sales"/>
                </div>
                <div class="rb-quarter-box">
                    <pie title="product sales" sub-title="last year" :legend="['产品1', '产品2', '产品3', '产品4', '产品5']" :series="this.pieData" item-name="sales"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import card from '@/components/item/card'
import linechart from '@/components/item/linechart'
import dashboard from '@/components/item/dashboard'
import pie from '@/components/item/pie'

export default {
    data() {
        return {
            cardMsg: "1",
            linechartData: {
                xAxis: [],
                yAxis: []
            },
            dashboardVal: "5",
            pieData: []
        }
    },
    mounted: function() {
        if (this.timer) {
            clearInterval(this.timer)
        } else {
            this.timer = setInterval(() => {
                this.cardMsg = Math.random().toFixed(2).toString()

                var xVals = []
                var yVals = []
                for (var i = 0; i < 20; i++) {
                    xVals.push(i)
                    yVals.push(Math.random().toFixed(2).toString())
                }
                this.linechartData = {xAxis: xVals, yAxis: yVals}

                this.dashboardVal = (Math.random() * 100).toFixed(2).toString()

                this.pieData = []
                for (var i = 0; i < 5; ++i) {
                    this.pieData.push({
                        name: "product" + (i + 1),
                        value: (Math.random() * 100).toFixed(2).toString()
                    })
                }
            }, 5000)
        }
    },
    components: {
        card,
        linechart,
        dashboard,
        pie
    }
}
</script>

<style>
.l-half-box {
    height: 100%;
    width: 50%;
    margin-top: 0%;
    margin-right: 0%;
    margin-bottom: 0%;
    margin-left: 0%;
    padding: 0;
    float: left;
    font-size: 3em;
}
.r-half-box {
    height: 100%;
    width: 49%;
    margin-top: 0%;
    margin-right: 0%;
    margin-bottom: 0%;
    margin-left: 1%;
    padding: 0;
    float: left;
    font-size: 3em;
}
.lt-quarter-box {
    height: 49%;
    width: 49%;
    margin-top: 0%;
    margin-right: 1.8%;
    margin-bottom: 1.8%;
    margin-left: 0%;
    padding: 0;
    float: left;
    font-size: 0.5em;
}
.rt-quarter-box {
    height: 49%;
    width: 49%;
    margin-top: 0%;
    margin-right: 0%;
    margin-bottom: 1.8%;
    margin-left: 0%;
    padding: 0;
    float: left;
    font-size: 0.5em;
}
.rb-quarter-box {
    height: 49%;
    width: 49%;
    margin-top: 0%;
    margin-right: 0%;
    margin-bottom: 0%;
    margin-left: 1.8%;
    padding: 0;
    float: left;
    font-size: 0.5em;
}
.lb-quarter-box {
    height: 49%;
    width: 49%; 
    margin-top: 0%;
    margin-right: 0%;
    margin-bottom: 0%;
    margin-left: 0%;
    padding: 0;
    float: left;
    font-size: 0.5em;
}
</style>
