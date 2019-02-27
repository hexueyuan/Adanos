<template>
    <el-menu default-active="1" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
        <el-submenu index="1">
            <template slot="title">
                <i class="el-icon-menu"></i>
                <span>系统监控</span>
            </template>
            <el-menu-item-group>
                <el-menu-item index="1-1">CPU数据</el-menu-item>
                <el-menu-item index="1-2">磁盘数据</el-menu-item>
            </el-menu-item-group>
        </el-submenu>
    </el-menu>
</template>

<script>
export default {}
</script>
