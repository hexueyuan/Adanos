<template>
    <el-card :id="cardId" class="data-card-item">
        <h1 class="data-card-item-title">{{ title }}</h1>
        <p :style="{ color: color }" class="data-card-item-data">{{ data }}</p>
    </el-card>
</template>

<script>
export default {
    props: {
        cardId: String,
        title: String,
        data: String,
        color: String
    }
}
</script>

<style>
.data-card-item {
    width: 24.8%;
    height: 28%;
    background-color: #404040;
    float: left;
}
.data-card-item-title {
    font-size: 4vh;
    margin: 0px;
    color: aliceblue;
}
.data-card-item-data {
    font-size: 6vh;
    text-align: center;
}
.el-card__body {
    padding: 0px;
}
</style>
