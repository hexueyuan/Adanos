<template>
    <div style="width: 100%;height: 100%;">
        <Card card-id="card1" title="Test1" data="value" color="green"/>
        <Card card-id="card2" title="Test2" data="value" color="red"/>
        <Card card-id="card3" title="Test3" data="value" color="yellow"/>
        <Card card-id="card4" title="Test4" data="value" color="blue"/>
    </div>
</template>

<script>
import Card from '@/components/charts/Card'

export default {
    components: {
        Card
    }
}
</script>
