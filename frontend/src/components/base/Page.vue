<template>
    <div id="page">
        <router-view></router-view>
    </div>
</template>

<script>
export default {
    //data() {
    //    return {
    //        websock: null
    //    }
    //},
    //created() {
    //    this.initWebSocket()
    //},
    //methods: {
    //    initWebSocket() {
    //        const wsuri = 'ws://localhost:8081'
    //        this.websock = new WebSocket(wsuri)
    //        this.websock.onopen = this.websocketonopen;
    //        this.websock.onerror = this.websocketonerror;
    //        this.websock.onmessage = this.websocketonmessage;
    //        this.websock.onclose = this.websocketonclose;
    //    },
    //    websocketonopen() {
    //        console.log("建立连接成功")
    //    },
    //    websocketonclose(e) {
    //        console.log("连接已经断开(" + e.code + ")")
    //    },
    //    websocketonerror(e) {
    //        console.log("连接出现错误")
    //    },
    //    websocketonmessage(e) {
    //        const redata = JSON.parse(e.data)
    //        console.log(redata)
    //    },
    //    connect() {
    //        this.websock.send('connect')
    //    }
    //}
}
</script>

<style>
#page {
    width: 100%;
    height: 100%;
    margin:0;
}
</style>
