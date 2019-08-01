// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));

myChart.showLoading();
$.getJSON('static/data/middle_school_extend.json' +'?timestamp='+ new Date().getTime(), function (json) {
    myChart.hideLoading();

    var categories = [];
    categories[0] = {
        name: '普通知识点'
    };
    categories[1] = {
        name: '算法相关'
    };

    // a dictionary define color of the links
    var link_color = {
        "contain": "#ff7f50",
        "arithmetic operation": "#87cefa",
        "property": "#da70d6",
        "algorithm": "#32cd32",
        "application": "#6495ed",
        "example": "#ff69b4",
        "expression": "#ba55d3",
        "theorem": "#cd5c5c",
        "conjecture": "#ffa500",
        "proof": "#40e0d0",
        "proof methods": "#1e90ff",
        "corollary": "#ff6347",
        "formula": "#7b68ee"
    };

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
                name: 'Math Knowledge Graph',
                type: 'graph',
                layout: 'force',
                data: json.nodes.map(function (node) {
                    return {
                        item_type: 'node', 
                        itemStyle: null,
                        symbolSize: node.viz.size / 1.5,
                        value: node.viz.size / 1.5,
                        label : {
                            normal: {
                                show: node.viz.size > 15
                            }
                        },
                        name: node.id,
                        degree: node.Degree,
                        id: node.id,
                        modular: node.modular,
                        // viz: node.viz,
                        category: node.modular 
                    };
                }),
                links: json.links.map(function (link) {
                    return {
                        item_type: 'edge',
                        id: link.id,
                        lineStyle: {
                            normal: {
                                color: link_color[link.relationship]
                            }
                        },
                        name: link.source + '->' + link.target,
                        source: link.source,
                        target: link.target,
                        category: link.relationship,
                    }
                }),
                categories: categories,
                roam: true,
                focusNodeAdjacency: true,
                draggable: true,
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
                lineStyle:  {
                    color: 'category',
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
});

myChart.on("click", function(params) {
    var data = params.data;
    console.log(data);
    var graphElem_table = document.getElementById("node info tbody");
    if (data.item_type == 'node') {
        graphElem_table.innerHTML = 
        '<tr>'
            + '<td>' + 'Name' + '</td>'
            + '<td>' + data.id + '</td>' +
        '</tr>';
    graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'Category' + '</td>'
            + '<td>' + data.category + '</td>' +
        '</tr>';
    graphElem_table.innerHTML += 
    '<tr>'
        + '<td>' + 'Degree' + '</td>'
        + '<td>' + data.degree + '</td>' +
    '</tr>';
    graphElem_table.innerHTML += 
    '<tr>'
        + '<td>' + 'Notes' + '</td>'
        + '<td>' + "" + '</td>' +
    '</tr>';
    } else {
    graphElem_table.innerHTML = 
    '<tr>'
        + '<td>' + 'Name' + '</td>'
        + '<td>' + data.name + '</td>' +
    '</tr>';
    graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'Source' + '</td>'
            + '<td>' + data.source + '</td>' +
        '</tr>';
    graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'Target' + '</td>'
            + '<td>' + data.target + '</td>' +
        '</tr>';
    graphElem_table.innerHTML += 
    '<tr>'
        + '<td>' + 'Relationship' + '</td>'
        + '<td>' + data.category + '</td>' +
    '</tr>';
    graphElem_table.innerHTML += 
    '<tr>'
        + '<td>' + 'Notes' + '</td>'
        + '<td>' + "" + '</td>' +
    '</tr>';     
    }
});