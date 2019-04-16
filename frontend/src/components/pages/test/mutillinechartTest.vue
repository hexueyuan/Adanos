<template>
    <div style="height:100%;width:100%">
        <div style="height: 50%;width:100%; margin-bottom:10px;float:left">
            <mutillinechart title="组件测试标题" sub-title="组件测试副标题" :legend="testdata.legend" :data="testdata.data"/>
        </div>
        <div style="height: 50%;width:49%; margin-bottom:10px;margin-right:10px;float:left;">
            <mutillinechart title="组件测试标题" sub-title="组件测试副标题" :legend="testdata.legend" :data="testdata.data"/>
        </div>
        <div style="height: 25%;width:50%; margin-bottom:10px;margin-right:10px;float:left;">
            <mutillinechart title="组件测试标题" sub-title="组件测试副标题" :legend="testdata.legend" :data="testdata.data"/>
        </div>
        <div style="height: 25%;width:50%; margin-bottom:10px;margin-right:10px;float:left;">
            <mutillinechart title="组件测试标题" sub-title="组件测试副标题" :legend="testdata.legend" :data="testdata.data"/>
        </div>
    </div>
</template>

<script>
import mutillinechart from '@/components/item/mutillinechart'

export default {
    components: {
        mutillinechart
    },
    data() {
        return {
            testdata: {
              legend: ['hour', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
              data: []
            }
        }
    },
    mounted() {
        if (this.timer) {
            clearInterval(this.timer)
        } else {
            this.timer = setInterval(() => {
                var data = [
                    ['测试组1'],
                    ['测试组2'],
                    ['测试组3'],
                    ['测试组4'],
                    ['测试组5']
                ]
                for (var i = 0; i < 24; i++) {
                    data[0].push((Math.random() * 100).toFixed(2).toString())
                    data[1].push((Math.random() * 100).toFixed(2).toString())
                    data[2].push((Math.random() * 100).toFixed(2).toString())
                    data[3].push((Math.random() * 100).toFixed(2).toString())
                    data[4].push((Math.random() * 100).toFixed(2).toString())
                }
                this.testdata.data = data
            }, 2000)
        }
    }
}
</script>