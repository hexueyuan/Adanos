//静态配置

const linechart_option = {
    title: {
        text: '',
        right: 'center'
    },
    tooltip: {
        trigger: 'axis'
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: []
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            data: [],
            type: 'line',
            smooth: true,
            areaStyle: {
                color: '#CAE1FF'
            },
            lineStyle: {
                color: '#CAE1FF'
            }
        }
    ]
}



const conf = {
    linechart_option
}

export default conf;