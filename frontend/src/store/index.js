import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    cpu: {
        //图表数据窗口大小默认20
        win_size: 20,
        //win_size * 1.2
        win_max_size: 24,
        //进程数据窗口大小默认10
        proccess_top_cnt: 10,
        //为适应动态调整，数据实际保存数量为win_size的1.2倍
        data: [
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0},
            {'timestamp': 0, 'logical_cnt': 0, 'phycisc_cnt': 0, 'used_rate': 0.0, 'user_time_percent': 0.0, 'system_time_percent': 0.0, 'idle_time_percent': 0.0}
        ]
    },
    disk: {
        //图表数据窗口大小默认20
        win_size: 20,
        //win_size * 1.2
        win_max_size: 24,
        //进程数据窗口大小默认10
        proccess_top_cnt: 10,
        //为适应动态调整，数据实际保存数量为win_size的1.2倍
        data: {}
    },
    memory: {
        //图表数据窗口大小默认20
        win_size: 20,
        //win_size * 1.2
        win_max_size: 24,
        //进程数据窗口大小默认10
        proccess_top_cnt: 10,
        //为适应动态调整，数据实际保存数量为win_size的1.2倍
        data: [
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0},
            {'timestamp': 0, 'mem_total': 0, 'mem_used_rate': 0, 'swap_total': 0, 'swap_used_rate': 0, 'swap_sin': 0, 'swap_sout': 0}
        ]
    },
    proccess: {
        //保存全部进程数据
        data: []
    }
}

const getters = {
    cpuData(state) {
        return state.cpu.data.slice(state.cpu.win_size * (-1))
    },
    diskData(state) {
        //var diskinfo = {}
        //for (var device in state.disk.data) {
        //    if (state.disk.data[device].length > state.disk.win_size) {
        //        diskinfo[device] = state.disk.data[device].slice(state.disk.win_size * (-1))
        //    } else {
        //        diskinfo[device] = state.disk.data[device]
        //    }
        //}
        //return diskinfo
        return state.disk.data
    },
    memoryData(state) {
        var meminfo = state.memory.data.slice(state.memory.win_size * (-1))
        meminfo.forEach(element => {
            element.mem_used = ((element.mem_total * element.mem_used_rate / 100) / (1024 * 1024 * 1024)).toFixed(2)
            element.mem_total = (element.mem_total / (1024 * 1024 * 1024)).toFixed(2)
            element.mem_free = (element.mem_total - element.mem_used).toFixed(2)
            element.swap_used = ((element.swap_total * element.swap_used_rate / 100) / (1024 * 1024 * 1024)).toFixed(2)
            element.swap_total = (element.swap_total / (1024 * 1024 * 1024)).toFixed(2)
            element.swap_free = (element.swap_total - element.swap_used).toFixed(2)
            element.swap_sin = (element.swap_sin / (1024 * 1024 * 1024)).toFixed(2)
            element.swap_sout = (element.swap_sout / (1024 * 1024 * 1024)).toFixed(2)
        })
        return meminfo
    },
    proccessCPUData(state) {
        var copyData = state.proccess.data.slice(0)
        copyData.sort((a, b) => {return b.cpu - a.cpu})
        return copyData.slice(state.cpu.proccess_top_cnt * (-1))
    }
}

const mutations = {
    updateCPUData(state, datas) {
        datas.forEach(element => {
            state.cpu.data.push(element)
            if (state.cpu.data.length > state.cpu.win_max_size) {
                state.cpu.data.shift()
            }
        });
    },
    updateDiskData(state, datas) {
        var tmp = state.disk.data
        state.disk.data = null
        state.disk.data = tmp
        datas.forEach(item => {
            if (!(item.device_name in state.disk.data)) {
                state.disk.data[item.device_name] = [item]
            } else {
                state.disk.data[item.device_name].push(item)
                if (state.disk.data[item.device_name].length > state.disk.win_max_size) {
                    state.disk.data[item.device_name].shift()
                }
            }
        })
    },
    updateMemoryData(state, datas) {
        datas.forEach(element => {
            state.memory.data.push(element)
            if (state.memory.data.length > state.memory.win_max_size) {
                state.memory.data.shift()
            }
        });
    },
    updateProccessData(state, datas) {
        state.proccess.data = datas
    }
}

const store = new Vuex.Store({
    state,
    getters,
    mutations
})

export default store;