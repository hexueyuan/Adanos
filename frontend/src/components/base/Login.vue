<template>
    <div id="login">
        <div id="login-box">
            <div id="title-box">
                <h1 id="title">
                    Adanos
                </h1>
                <h2 id="subtitle">
                    登录Adanos
                </h2>
            </div>
            <el-card id="login-main">
                <div id="username-box">
                    <p id="username-tips">用户名</p>
                    <el-input id="username" v-model="username" placeholder=""></el-input>
                </div>
                <div id="password-box">
                    <p id="password-tips">密码</p>
                    <el-input id="password-box" v-model="password" placeholder="" show-password></el-input>
                </div>
                <div id="commit-box">
                    <el-button id="commit" type="success" @click="login">登录</el-button>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        login() {
            if (this.username === "adanos" && this.password === "password") {
                this.$router.push('/Adanos')
            } else {
                alert('密码错误')
            }
        }
    }
}
</script>

<style>
#login {
    height: 100%;
    width: 100%;
    background: url('/static/svg/simple-codelines.svg'), #2b3137;
}
#login-box {
    height:600px;
    width:400px;
    display: table;
    margin: 0 auto;
}
#login-main {
    width: 100%;
    display: table-cell;
    vertical-align: middle;
    float: left;
}
#title-box {
    width: 100%;
    height: 200px;
    float: left;
}
#title {
    color: rgb(238, 234, 234);
}
#subtitle {
    color: rgb(238, 234, 234);
}
#username-box {
    margin-top: 10px;
}
#username-tips {
    margin-bottom: 5px;
}
#username {
    margin-top: 0px;
}
#password-tips {
    margin-bottom: 5px;
}
#password-box {
    margin-top: 10px;
}
#password {
    margin-top: 0px;
}
#commit-box {
    margin-top: 10px;
}
#commit {
    margin: 0 auto;
}
</style>
