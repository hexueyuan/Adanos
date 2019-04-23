<template>
    <el-card  class="card" shadow="hover">
        <div slot="header">
            <span class="card-title">{{ title }}</span>
        </div>
        <div>
            <span class="card-value">{{ value }}</span>
        </div>
    </el-card>
</template>

<script>
export default {
    props: {
        value: String,
        title: String
    }
}
</script>

<style>
/* 卡片 */
.card {
    height: 100%;
    width: 100%;
}
.card-value {
    font-size: 48px;
    color: black;
    text-align: center;
}
.card-title {
    font-size: 24px;
    color: black;
}
</style>
