// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));

myChart.showLoading();
$.get('static/data/middle_school_extend_0.gexf', function (xml) {
    myChart.hideLoading();

    var graph = echarts.dataTool.gexf.parse(xml);
    var categories = [];
    categories[0] = {
        name: '普通知识点'
    };
    categories[1] = {
        name: '算法相关'
    };
    // for (var i = 0; i < 2; i++) {
    //     categories[i] = {
    //         name: '算法' + i
    //     };
    // }
    graph.nodes.forEach(function (node) {
        node.itemStyle = null;
        node.value = node.symbolSize;
        node.symbolSize /= 1.5;
        node.label = {
            normal: {
                show: node.symbolSize > 30
            }
        };
        node.category = node.attributes.modular;
    });
    option = {
        title: {
            text: 'Math KG',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right'
        },
        tooltip: {},
        legend: [{
            // selectedMode: 'single',
            data: [
                '普通知识点',
                {
                    name: '算法相关'
                }]
        }],
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',
        series : [
            {
                // name: 'Math Knowledge Graph',
                type: 'graph',
                layout: 'force',
                data: graph.nodes,
                links: graph.links,
                categories: categories,
                roam: true,
                focusNodeAdjacency: true,
                // draggable: true,
                force: {
                    repulsion: 1000
                },
                itemStyle: {
                    normal: {
                        borderColor: '#fff',
                        borderWidth: 1,
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.3)'
                    }
                },
                label: {
                    position: 'right',
                    formatter: '{b}'
                },
                lineStyle: {
                    color: 'source',
                    curveness: 0.3
                },
                emphasis: {
                    lineStyle: {
                        width: 10
                    }
                }
            }
        ]
    };

    myChart.setOption(option);
}, 'xml');

myChart.on("click", function(params) {
    var data = params.data;
    console.log(data);
    var graphElem_table = document.getElementById("node info tbody");
    graphElem_table.innerHTML = 
        '<tr>'
            + '<td>' + 'Name' + '</td>'
            + '<td>' + data.name + '</td>' +
        '</tr>';
    graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'ID' + '</td>'
            + '<td>' + data.id + '</td>' +
        '</tr>';
});