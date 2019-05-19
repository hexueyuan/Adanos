<template>
    <div class="item">
        <img :src="imgPath" class="item-icon"/>
        <p class="item-name">{{ itemName }}</p>
    </div>
</template>

<script>
export default {
    props: {
        type: String,
        itemName: String
    },
    data() {
        return {
            imgPath: this.typeMap(this.type, this.itemName)
        }
    },
    methods: {
        typeMap: function(type, name) {
            if (type == "directory") {
                return "./static/img/directory.png"
            } else {
                return "./static/img/text.png"
            }
        }
    }
}
</script>

<style>
.item {
    height: 120px;
    width: 120px;
}
.item:hover {
    background-color:gray;
}
.item-icon {
    height: 80px;
    width: 80px;
    margin: 0 auto;
}
.item-icon:hover {
    height: 85px;
    width: 85px;
}
.item-name {
    text-align: center;
    font-size: 12px;
    margin: 0 auto;
}
</style>
