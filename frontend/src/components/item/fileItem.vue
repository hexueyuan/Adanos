<template>
    <div class="item" :name="itemName" :type="type">
        <img :src="imgPath" class="item-icon" :name="itemName" :type="type"/>
        <p class="item-name" :name="itemName" :type="type">{{ itemName }}</p>
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
    background-color:rgb(221, 217, 217);
    border-radius:5px;
}
.item-icon {
    height: 80px;
    width: 80px;
    margin-left: 20px;
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
