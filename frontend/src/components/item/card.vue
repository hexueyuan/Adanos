<template>
    <el-card  :style="{ backgroundColor: color }" shadow="hover">
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
        title: String,
        color: String
    },
    data() {
        return {
            icon: "meh"
        }
    },
    mounted() {
        if (this.type == "good") {
            this.icon = "smile"
        } else if (this.type == "warning") {
            this.icon = "frown"
        } else if (this.type == "bad") {
            this.icon = "close-circle"
        } else {
            this.icon = "meh"
        }
    }
}
</script>

<style>
/* 卡片 */
.card {
    height: 100%;
    width: 100%;
    border-radius: 8px;
    -webkit-border-radius: 8px;
    -moz-border-radius: 8px;
    -webkit-box-shadow: #666 0px 0px 10px;
    -moz-box-shadow: #666 0px 0px 10px;
    box-shadow: #666 0px 0px 10px;
}
.card-icon-div {
    height: 100%;
    width: 40%;
    float: left;
    position:relative; 
}
.card-data-div {
    height: 100%;
    width: 60%;
    float: left;
    position:relative;
}
.card-icon {
    font-size: 72px;
    color: white;
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%) !important;
}
.card-value {
    font-size: 24px;
    color: black;
}
.card-title {
    font-size: 24px;
    color: black;
}
/**==================**/
/*不同类型卡片背景色*/

/*good类型的卡片*/
.card-good {
    background-color: #36dd8a;
}

/*warning类型卡片*/
.card-warning {
    background-color: #e6dc51;
}

/*bad类型卡片*/
.card-bad {
    background-color: #fc796a;
}

/*common类型卡片*/
.card-common {
    background-color: #5f7fb6;
}
</style>
