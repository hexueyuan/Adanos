<template>
    <div style="height:100%;width:100%;">
        <div style="height:80%;width:100%;border: 2px solid #000;margin-bottom: 10px;float:left;">
            <pie title="product sales" sub-title="last year" :legend="legend" :data="this.pieData"/>
        </div>
        <div style="height:80%;width:50%;border: 2px solid #000;margin-bottom:10px;float:left;margin-right: 10px;">
            <pie title="product sales" sub-title="last year" :legend="legend" :data="this.pieData"/>
        </div>
        <div style="height:80%;width:49.3%;margin-bottom:10px;float:left;">
            <div style="height: 50%;width:100%;border: 2px solid #000;margin-bottom:10px;">
                <pie title="product sales" sub-title="last year" :legend="legend" :data="this.pieData"/>
            </div>
            <div style="height: 49%;width:100%;border: 2px solid #000;">
                <pie title="product sales" sub-title="last year" :legend="legend" :data="this.pieData"/>
            </div>
        </div>
        <div style="height:80%;width:50%;margin-right:10px;margin-bottom:10px;float:left;">
            <div style="height:100%;width:49.2%;border: 2px solid #000;margin-right:10px;float:left;">
                <pie title="product sales" sub-title="last year" :legend="legend" :data="this.pieData"/>
            </div>
            <div style="height:100%;width:49.2%;border: 2px solid #000;float:left;">
                <pie title="product sales" sub-title="last year" :legend="legend" :data="this.pieData"/>
            </div>
        </div>
        <div style="height:80%;width:49.3%;margin-bottom:10px;float:left;">
            <div style="height:49.4%;width;100%;margin-bottom:10px;">
                <div style="height:100%;width:49.1%;margin-right:10px;float:left;border: 2px solid #000;">
                    <pie title="product sales" sub-title="last year" :legend="legend" :data="this.pieData"/>
                </div>
                <div style="height:100%;width:49.1%;float:left;border: 2px solid #000;">
                    <pie title="product sales" sub-title="last year" :legend="legend" :data="this.pieData"/>
                </div>
            </div>
            <div style="height:49.4%;width;100%;">
                <div style="height:100%;width:49.1%;margin-right:10px;float:left;border: 2px solid #000;">
                    <pie title="product sales" sub-title="last year" :legend="legend" :data="this.pieData"/>
                </div>
                <div style="height:100%;width:49.1%;float:left;border: 2px solid #000;">
                    <pie title="product sales" sub-title="last year" :legend="legend" :data="this.pieData"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import pie from '@/components/item/pie'
export default {
    components: {
        pie
    },
    data() {
        return {
            pieData: [],
            legend: ['product1', 'product2', 'product3', 'product4', 'product5']
        }
    },
    mounted() {
        if (this.timer) {
            clearInterval(this.timer)
        } else {
            this.timer = setInterval(() => {
                this.pieData = []
                for (var i = 0; i < 5; ++i) {
                    this.pieData.push({
                        name: "product" + (i + 1),
                        value: (Math.random() * 100).toFixed(2).toString()
                    })
                }
            }, 2000)
        }
    }
}
</script>