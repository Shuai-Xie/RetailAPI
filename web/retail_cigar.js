// init myChart div
let myChart = echarts.init(document.getElementById('chart'));
myChart.showLoading();

// read json data
$.get('../data/retail_stats_echart.json', function (data) {
    // data structure for bar charts

    cigar_dict = data['children'][0]['children'].map(function (item) {
                return [item['name'], item['value']]
    });
    // sort the dict
    cigar_dict.sort(function(first, second) {
        return second[1] - first[1];
    });
    cigar_dict.reverse();

    // console.log(cigar_dict);

    cigar_data_ordered = {}
    cigar_data_ordered['cats'] = cigar_dict.map(function (item) {
                return item[0];
    });
    cigar_data_ordered['nums'] = cigar_dict.map(function (item) {
                return item[1];
    });
    max_num = cigar_data_ordered['nums'][cigar_data_ordered['nums'].length-1]
    // console.log(max_num)
    // console.log(cigar_data_ordered['cats']);

    // console.log(cigar_data);
    myChart.hideLoading();
    myChart.setOption(option = {
        title: {
            top: 5,
            left: 'center',
            text: 'Retail Cigar Dataset Statistics',
            subtext:  'classes: ' + data['children'][0]['children'].length + ', instances: ' + data['children'][0]['value'] + ' )',
        },
        tooltip: {
            trigger: 'item',
            triggerOn: 'mousemove'
        },
        legend: {
            top: 55,
            left: 'center',  // 'center' 居中, 'x' 左对齐
            // orient: 'vertical',
            data: [
                '香烟',
            ],
            icon: 'circle',
        },
        grid: [ // stats 子图位置
            { // cigar
                top: 120,
                bottom: '5%',
                left: '10%',
                right: '10%',
                // containLabel: true
            },
        ],

        xAxis: [
            {
                type: 'value',
                name: 'amount',
                max: max_num,
            },
        ],

        yAxis: [
            {
                type: 'category',
                name: '香烟',
                data: cigar_data_ordered['cats'],
            },
        ],

        series: [
            {
                name: '香烟',
                type: 'bar',
                // barWidth: 5,
                data: cigar_data_ordered['nums'],
                label: {
                    normal: {
                        position: 'right',
                        fontSize: 12, // 右侧数字大小
                        show: true,
                    }
                },
            },
        ]
    });
});
$(window).resize(function () {
    myChart.resize();
});