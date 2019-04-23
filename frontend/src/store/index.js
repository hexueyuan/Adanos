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
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0},
            {'load': 0, 'user': 0, 'system': 0, 'idle': 0, 'nice': 0, 'time': 0}
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
        data: [
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0},
            {'use_rate': 0, 'total': 0, 'used': 0, 'free': 0, 'active': 0, 'inactive': 0, 'time': 0}
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
        return state.disk.data.slice(state.disk.win_size * (-1))
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
        datas.forEach(element => {
            state.disk.data.push(element)
            if (state.disk.data.length > state.disk.win_max_size) {
                state.disk.data.shift()
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