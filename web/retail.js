// init myChart div
let myChart = echarts.init(document.getElementById('chart'));
myChart.showLoading();


// read json data
$.get('../data/retail_stats_echart.json', function (data) {
    // data structure for bar charts
    let data_stats = {};
    // map 代替 list 中的 for 语句
    data['children'].map(function (super_cats) {
        super_cats['children'] = super_cats['children'].reverse(); // reverse 反向，使得柱状图 类别自上而下
        data_stats[super_cats['name']] = {
            'cats': super_cats['children'].map(function (item) {
                return item['name'];
            }),
            'nums': super_cats['children'].map(function (item) {
                return item['value'];
            }),
        }
    });

    // echarts.util.each(data.children, function (datum, index) {
    //     index > 0 && (datum.collapsed = true); // 只显示烟
    // });

    myChart.hideLoading();
    myChart.setOption(option = {
        title: {
            top: 5,
            left: 'center',
            text: 'Retail Products Dataset Statistics',
            subtext: '( images: ' + data['images'] + ', classes: ' + data['classes'] + ', instances: ' + data['instances'] + ' )',
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
                'class tree',
                '香烟',
                '饮料',
                '酒水',
                '零食',
                '牛奶',
                '文具',
                '日用品',
                '食物',
                '玩具', // add
            ],
            icon: 'circle',
        },
        grid: [ // stats 子图位置
            { // cigar
                top: 120,
                bottom: '65%',
                left: '60%',
                right: '10%',
                // containLabel: true
            },
            { // drink
                top: '37%',
                bottom: '50%',
                left: '60%',
                right: '10%',
                // containLabel: true
            },
            { // alcohol
                top: '52%',
                bottom: '47%',
                left: '60%',
                right: '10%',
                // containLabel: true
            },
            { // snack
                top: '55%',
                bottom: '35%',
                left: '60%',
                right: '10%',
                // containLabel: true
            },
            { // milk
                top: '67%',
                bottom: '26%',
                left: '60%',
                right: '10%',
                // containLabel: true
            },
            { // stationery
                top: '76%',
                bottom: '22%',
                left: '60%',
                right: '10%',
                // containLabel: true
            },
            { // daily_supplies
                top: '80%',
                bottom: '18%',
                left: '60%',
                right: '10%',
                // containLabel: true
            },
            { // food
                top: '84%',
                bottom: '12%',
                left: '60%',
                right: '10%',
                // containLabel: true
            },
            { // plaything 这个是你添加的 玩具吗？ 我不小心
                top: '90%',
                bottom: '6%',
                left: '60%',
                right: '10%',
                // containLabel: true
            },
        ],

        xAxis: [
            {
                type: 'value',
                name: 'amount',
                max: 100,
            },
            {
                gridIndex: 1,
                type: 'value',
                name: 'amount',
                max: 100,
            },
            {
                gridIndex: 2,
                type: 'value',
                name: 'amount',
                max: 100,
            },
            {
                gridIndex: 3,
                type: 'value',
                name: 'amount',
                max: 100,
            },
            {
                gridIndex: 4,
                type: 'value',
                name: 'amount',
                max: 100,
            },
            {
                gridIndex: 5,
                type: 'value',
                name: 'amount',
                max: 100,
            },
            {
                gridIndex: 6,
                type: 'value',
                name: 'amount',
                max: 100,
            },
            {
                gridIndex: 7,
                type: 'value',
                name: 'amount',
                max: 100,
            },
            {
                gridIndex: 8,
                type: 'value',
                name: 'amount',
                max: 100,
            },
        ],

        yAxis: [
            {
                type: 'category',
                name: '香烟',
                data: data_stats['cigar']['cats'],
            },
            {
                gridIndex: 1,
                type: 'category',
                name: '饮料',
                data: data_stats['drink']['cats'],
            },
            {
                gridIndex: 2,
                type: 'category',
                name: '酒水',
                data: data_stats['alcohol']['cats'],
            },
            {
                gridIndex: 3,
                type: 'category',
                name: '零食',
                data: data_stats['snack']['cats'],
            },
            {
                gridIndex: 4,
                type: 'category',
                name: '牛奶',
                data: data_stats['milk']['cats'],
            },
            {
                gridIndex: 5,
                type: 'category',
                name: '文具',
                data: data_stats['stationery']['cats'],
            },
            {
                gridIndex: 6,
                type: 'category',
                name: '日用品',
                data: data_stats['daily_supplies']['cats'],
            },
            {
                gridIndex: 7,
                type: 'category',
                name: '食物',
                data: data_stats['food']['cats'],
            },
            {
                gridIndex: 8,
                type: 'category',
                name: '玩具',
                data: data_stats['plaything']['cats'],
            },
        ],

        series: [
            {
                name: 'class tree',
                type: 'tree',
                // 设置 legend 和 tree color
                itemStyle: {
                    color: ['#d9534f'],
                    borderColor: ['#d43f3a'],
                },
                data: [data],
                // tree 位置
                top: 100,
                bottom: '1%',
                left: '15%',
                right: '60%',
                symbolSize: 7,
                label: {
                    normal: {
                        position: 'left',
                        verticalAlign: 'bottom',  // 'middle',
                        align: 'right',
                        fontSize: 12,
                        // 显示 value 值
                        formatter: function (params) {
                            if (params.value > 0)
                                return params.name + ': ' + params.value;
                            else
                                return params.name
                        }
                    }
                },
                leaves: {
                    label: {
                        normal: {
                            position: 'right',
                            verticalAlign: 'middle',
                            align: 'left',
                        },
                    }
                },
                expandAndCollapse: true,
                animationDuration: 550,
                animationDurationUpdate: 750
            },

            {
                name: '香烟',
                type: 'bar',
                // barWidth: 5,
                data: data_stats['cigar']['nums'],
                label: {
                    normal: {
                        position: 'right',
                        fontSize: 12, // 右侧数字大小
                        show: true,
                    }
                },
            },

            {
                name: '饮料',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: data_stats['drink']['nums'],
                label: {
                    normal: {
                        position: 'right',
                        fontSize: 12, // 右侧数字大小
                        show: true,
                    }
                },
            },

            {
                name: '酒水',
                type: 'bar',
                xAxisIndex: 2,
                yAxisIndex: 2,
                data: data_stats['alcohol']['nums'],
                label: {
                    normal: {
                        position: 'right',
                        fontSize: 12, // 右侧数字大小
                        show: true,
                    }
                },
            },

            {
                name: '零食',
                type: 'bar',
                xAxisIndex: 3,
                yAxisIndex: 3,
                data: data_stats['snack']['nums'],
                label: {
                    normal: {
                        position: 'right',
                        fontSize: 12, // 右侧数字大小
                        show: true,
                    }
                },
            },

            {
                name: '牛奶',
                type: 'bar',
                xAxisIndex: 4,
                yAxisIndex: 4,
                data: data_stats['milk']['nums'],
                label: {
                    normal: {
                        position: 'right',
                        fontSize: 12, // 右侧数字大小
                        show: true,
                    }
                },
            },

            {
                name: '文具',
                type: 'bar',
                xAxisIndex: 5,
                yAxisIndex: 5,
                data: data_stats['stationery']['nums'],
                label: {
                    normal: {
                        position: 'right',
                        fontSize: 12, // 右侧数字大小
                        show: true,
                    }
                },
            },

            {
                name: '日用品',
                type: 'bar',
                xAxisIndex: 6,
                yAxisIndex: 6,
                data: data_stats['daily_supplies']['nums'],
                label: {
                    normal: {
                        position: 'right',
                        fontSize: 12, // 右侧数字大小
                        show: true,
                    }
                },
            },

            {
                name: '食物',
                type: 'bar',
                xAxisIndex: 7,
                yAxisIndex: 7,
                data: data_stats['food']['nums'],
                label: {
                    normal: {
                        position: 'right',
                        fontSize: 12, // 右侧数字大小
                        show: true,
                    }
                },
            },

            {
                name: '玩具',
                type: 'bar',
                xAxisIndex: 8,
                yAxisIndex: 8,
                data: data_stats['plaything']['nums'],
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

