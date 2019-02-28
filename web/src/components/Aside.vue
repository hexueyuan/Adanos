<template>
<el-row class="tac">
    <el-menu default-active="1" class="el-menu-vertical-demo" background-color="#545c64"  active-text-color="#ffd04b">
        <el-menu-item index="0">
            <i class="el-icon-document"></i>
            <span slot="title"><router-link to="/" class="menu-option1">主页</router-link></span>
        </el-menu-item>
        <el-submenu index="1">
            <template slot="title">
                <i class="el-icon-menu"></i>
                <span class="menu-option1">系统监控</span>
            </template>
            <el-menu-item-group>
                <el-menu-item index="1-1"><span class="menu-option2">CPU数据</span></el-menu-item>
                <el-menu-item index="1-2"><router-link to="/system/disk_use_rate" class="menu-option2">磁盘数据</router-link></el-menu-item>
            </el-menu-item-group>
        </el-submenu>
    </el-menu>
</el-row>
</template>

<script>
export default {}
</script>

<style>
.menu-option1 {
    text-decoration:none;
    color: white;
    font-size: 18px;
}
.menu-option2 {
    text-decoration:none;
    color: white;
    font-size: 16px;
}
</style>