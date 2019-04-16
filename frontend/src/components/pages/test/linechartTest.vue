<template>
    <div style="height:100%;width:100%;">
        <div style="height:80%;width:100%;border: 2px solid #000;margin-bottom: 10px;float:left;">
            <linechart title="测试组件" :data="data"/>
        </div>
        <div style="height:80%;width:50%;border: 2px solid #000;margin-bottom:10px;float:left;margin-right: 10px;">
            <linechart title="测试组件" :data="data"/>
        </div>
        <div style="height:80%;width:49.3%;margin-bottom:10px;float:left;">
            <div style="height: 50%;width:100%;border: 2px solid #000;margin-bottom:10px;">
                <linechart title="测试组件" :data="data"/>
            </div>
            <div style="height: 49%;width:100%;border: 2px solid #000;">
                <linechart title="测试组件" :data="data"/>
            </div>
        </div>
        <div style="height:80%;width:50%;margin-right:10px;margin-bottom:10px;float:left;">
            <div style="height:100%;width:49.2%;border: 2px solid #000;margin-right:10px;float:left;">
                <linechart title="测试组件" :data="data"/>
            </div>
            <div style="height:100%;width:49.2%;border: 2px solid #000;float:left;">
                <linechart title="测试组件" :data="data"/>
            </div>
        </div>
        <div style="height:80%;width:49.3%;margin-bottom:10px;float:left;">
            <div style="height:49.4%;width;100%;margin-bottom:10px;">
                <div style="height:100%;width:49.1%;margin-right:10px;float:left;border: 2px solid #000;">
                    <linechart title="测试组件" :data="data"/>
                </div>
                <div style="height:100%;width:49.1%;float:left;border: 2px solid #000;">
                    <linechart title="测试组件" :data="data"/>
                </div>
            </div>
            <div style="height:49.4%;width;100%;">
                <div style="height:100%;width:49.1%;margin-right:10px;float:left;border: 2px solid #000;">
                    <linechart title="测试组件" :data="data"/>
                </div>
                <div style="height:100%;width:49.1%;float:left;border: 2px solid #000;">
                    <linechart title="测试组件" :data="data"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import linechart from '@/components/item/linechart'
export default {
    components: {
        linechart
    },
    data() {
        return {
            data: {
                xAxis: [],
                yAxis: []
            }
        }
    },
    mounted() {
        if (this.timer) {
            clearInterval(this.timer)
        } else {
            this.timer = setInterval(() => {
                var xVals = []
                var yVals = []
                for (var i = 0; i < 20; i++) {
                    xVals.push(i)
                    yVals.push(Math.random().toFixed(2).toString())
                }
                this.data = {xAxis: xVals, yAxis: yVals}
            }, 2000)
        }
    }
}
</script>