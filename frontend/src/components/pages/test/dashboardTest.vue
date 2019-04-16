<template>
    <div style="height:100%;width:100%;">
        <div style="height:80%;width:100%;border: 2px solid #000;margin-bottom: 10px;float:left;">
            <dashboard name="测试组件" :value="value"/>
        </div>
        <div style="height:80%;width:50%;border: 2px solid #000;margin-bottom:10px;float:left;margin-right: 10px;">
            <dashboard name="测试组件" :value="value"/>
        </div>
        <div style="height:80%;width:49.3%;margin-bottom:10px;float:left;">
            <div style="height: 50%;width:100%;border: 2px solid #000;margin-bottom:10px;">
                <dashboard name="测试组件" :value="value"/>
            </div>
            <div style="height: 49%;width:100%;border: 2px solid #000;">
                <dashboard name="测试组件" :value="value"/>
            </div>
        </div>
        <div style="height:80%;width:50%;margin-right:10px;margin-bottom:10px;float:left;">
            <div style="height:100%;width:49.2%;border: 2px solid #000;margin-right:10px;float:left;">
                <dashboard name="测试组件" :value="value"/>
            </div>
            <div style="height:100%;width:49.2%;border: 2px solid #000;float:left;">
                <dashboard name="测试组件" :value="value"/>
            </div>
        </div>
        <div style="height:80%;width:49.3%;margin-bottom:10px;float:left;">
            <div style="height:49.4%;width;100%;margin-bottom:10px;">
                <div style="height:100%;width:49.1%;margin-right:10px;float:left;border: 2px solid #000;">
                    <dashboard name="测试组件" :value="value"/>
                </div>
                <div style="height:100%;width:49.1%;float:left;border: 2px solid #000;">
                    <dashboard name="测试组件" :value="value"/>
                </div>
            </div>
            <div style="height:49.4%;width;100%;">
                <div style="height:100%;width:49.1%;margin-right:10px;float:left;border: 2px solid #000;">
                    <dashboard name="测试组件" :value="value"/>
                </div>
                <div style="height:100%;width:49.1%;float:left;border: 2px solid #000;">
                    <dashboard name="测试组件" :value="value"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import dashboard from '@/components/item/dashboard'
export default {
    components: {
        dashboard
    },
    data() {
        return {
            value: '0'
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