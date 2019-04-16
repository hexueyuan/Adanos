<template>
    <div style="height:100%;width:100%;">
        <div style="height:10%;width:100%;margin-bottom: 10px;float:left;">
            <card title="测试组件" :value="value" type="warning"/>
        </div>
        <div style="height:40%;width:50%;margin-bottom:10px;float:left;margin-right: 15px;">
            <card title="测试组件" :value="value" type="bad"/>
        </div>
        <div style="height:19.6%;width:49.3%;margin-bottom:10px;float:left;">
            <div style="height: 48%;width:100%;margin-bottom:10px;">
                <card title="测试组件" :value="value" type="common"/>
            </div>
            <div style="height: 48%;width:100%;">
                <card title="测试组件" :value="value" type="good"/>
            </div>
        </div>
        <div style="height:19.6%;width:49.3%;margin-bottom:10px;float:left;">
            <div style="height: 48%;width:100%;margin-bottom:10px;">
                <card title="测试组件" :value="value" type="warning"/>
            </div>
            <div style="height: 48%;width:100%;">
                <card title="测试组件" :value="value" type="bad"/>
            </div>
        </div>
        <div style="height:40%;width:100%;margin-bottom:10px;float:left;margin-right: 15px;">
            <card title="测试组件" :value="value" type="common"/>
        </div>
    </div>
</template>

<script>
import card from '@/components/item/card'
export default {
    components: {
        card
    },
    data() {
        return {
            value: ''
        }
    },
    mounted() {
        if (this.timer) {
            clearInterval(this.timer)
        } else {
            this.timer = setInterval(() => {
                this.value = (Math.random() * 100).toFixed(2).toString()
            }, 2000)
        }
    }
}
</script>