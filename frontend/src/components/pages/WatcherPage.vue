<template>
    <div>
        <div class="select-box">
            <el-row>
                <el-radio-group v-model="radio" style="float:left">
                    <el-radio-button label="实时"></el-radio-button>
                    <el-radio-button label="近24小时"></el-radio-button>
                    <el-radio-button label="近7天"></el-radio-button>
                    <el-radio-button label="选择时间"></el-radio-button>
                </el-radio-group>
                <div class="block">
                    <el-date-picker
                        v-model="time"
                        type="datetimerange"
                        range-separator="至"
                        start-placeholder="开始时间"
                        end-placeholder="结束时间">
                    </el-date-picker>
                </div>
            </el-row>
        </div>
        <div class="watcher-chart"></div>
        <div class="watcher-data-items"></div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            radio: '实时',
            time: [new Date(2000, 10, 10, 10, 10), new Date(2000, 10, 11, 10, 10)]
        }
    }
}
</script>
