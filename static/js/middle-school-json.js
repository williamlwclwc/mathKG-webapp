// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.getElementById('main'));

var GexfJS = {
    params: {
        activeNode: -1
    },
    graph: {
        nodeList: [],
        indexOfLabels: [],
        edgeList: [],
    }
};

myChart.showLoading();
$.getJSON('static/data/graph_from_mongodb.json' +'?timestamp='+ new Date().getTime(), function (json) {
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

    var graph = {
        nodes: json.nodes.map(function (node) {
            GexfJS.graph.indexOfLabels.push(node.id.toLowerCase());
            if (node.category == "0"){
                node.category = 0;
            }else{
                node.category = 1;
            }
            return {
                item_type: 'node', 
                itemStyle: null,
                value: node.viz.size,
                symbolSize: node.viz.size * 1.0,
                label : {
                    normal: {
                        // show: node.viz.size > 15
                        show: node.degree > 6
                    },
                    emphasis: {
                        show: true
                    }
                },
                name: node.id,
                id: node.id,
                url: node.wiki_url,
                category: node.category,
                degree: node.degree,
                viz: node.viz,
                content: node.content,
                notes: node.notes 
            };
        }),
        edges: json.links.map(function (link) {
            return {
                item_type: 'edge',
                id: link.id,
                lineStyle: {
                    color: link_color[link.relationship]
                },
                // name: link.source + '->' + link.target,
                value: link.value,
                key: link.key,
                source: link.source,
                target: link.target,
                relationship: link.relationship,
                content: link.content,
                notes: link.notes,
            }
        }),
    };

    GexfJS.graph.nodeList = graph.nodes;
    GexfJS.graph.edgeList = graph.links;

    option = {
        // title: {
        //     text: 'Math KG',
        //     subtext: 'Default layout',
        //     top: 'bottom',
        //     left: 'right'
        // },
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
                data: graph.nodes,
                links: graph.edges,
                categories: categories,
                roam: true,
                focusNodeAdjacency: true,
                draggable: true,
                force: {
                    initLayout: 'circular',
                    repulsion: [1000, 5000],
                    gravity: 0.01,
                    edgeLength: [0.01, 100]
                },
                // forceAtlas2: {
                //     steps: 1,
                //     stopThreshold: 20,
                //     jitterTolerence: 10,
                //     gravity: 10,
                //     scaling: 50,
                //     preventOverlap: true
                // },
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
                    // color: link_color[links.relationship],
                    curveness: 0.25
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
            + '<td>' + 'Type' + '</td>'
            + '<td>' + data.item_type + '</td>' +
        '</tr>';
        graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'Name' + '</td>'
            + '<td>' + data.id + '</td>' +
        '</tr>';
        graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'Category' + '</td>'
            + '<td>' + data.category + '</td>' +
        '</tr>';
        if (data.url != 'Not included in Wikipedia'){
            graphElem_table.innerHTML += 
            '<tr>'
                + '<td>' + 'Url' + '</td>'
                + '<td>' + '<a href='+ data.url +' target="_blank">'+ data.id +'</a>' + '</td>' +
            '</tr>';
        }
        graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'Degree' + '</td>'
            + '<td>' + data.degree + '</td>' +
        '</tr>';
        graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'Content' + '</td>'
            + '<td>' + data.content + '</td>' +
        '</tr>';
        graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'Notes' + '</td>'
            + '<td>' + data.notes + '</td>' +
        '</tr>';
    } else {
        graphElem_table.innerHTML = 
        '<tr>'
            + '<td>' + 'Type' + '</td>'
            + '<td>' + data.item_type + '</td>' +
        '</tr>';
        graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'ID(key)' + '</td>'
            + '<td>' + data.key + '</td>' +
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
            + '<td>' + data.relationship + '</td>' +
        '</tr>';
        graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'Content' + '</td>'
            + '<td>' + data.content + '</td>' +
        '</tr>';
        graphElem_table.innerHTML += 
        '<tr>'
            + '<td>' + 'Notes' + '</td>'
            + '<td>' + data.notes + '</td>' +
        '</tr>';     
    }
    var mathj = document.getElementById("node info body");
    // MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
	MathJax.Hub.Queue(["Typeset", MathJax.Hub, mathj]);
});

//search nodes
function highlight(_nodeIndex){
    myChart.dispatchAction({
        type: "focusNodeAdjacency",
        seriesIndex: 0,
        dataIndex: _nodeIndex
    });
}

$(document).ready(function () {

    $("#searchinput")
        .focus(function () {
            if ($(this).is('.grey')) {
                $(this).val('').removeClass('grey');
            }
        })
        .keyup(function (evt) {
            updateAutoComplete(this);
        }).keydown(function (evt) {
            var _l = $("#autocomplete li").length;
            switch (evt.keyCode) {
                case 40:
                    if (GexfJS.autoCompletePosition < _l - 1) {
                        GexfJS.autoCompletePosition++;
                    } else {
                        GexfJS.autoCompletePosition = 0;
                    }
                    break;
                case 38:
                    if (GexfJS.autoCompletePosition > 0) {
                        GexfJS.autoCompletePosition--;
                    } else {
                        GexfJS.autoCompletePosition = _l - 1;
                    }
                    break;
                case 27:
                    $("#autocomplete").slideUp();
                    break;
                case 13:
                    if ($("#autocomplete").is(":visible")) {
                        var _liac = $("#liac_" + GexfJS.autoCompletePosition);
                        if (_liac.length) {
                            $(this).val(_liac.text());
                        }
                    }
                    break;
                default:
                    GexfJS.autoCompletePosition = 0;
                    break;
            }
            updateAutoComplete(this);
            if (evt.keyCode == 38 || evt.keyCode == 40) {
                return false;
            }
        });
    $("#recherche").submit(function () {
        if (GexfJS.graph) {
            //displayNode(GexfJS.graph.indexOfLabels.indexOf($("#searchinput").val().toLowerCase()), true);
            highlight(GexfJS.graph.indexOfLabels.indexOf($("#searchinput").val().toLowerCase()));
        }
        return false;
    });
    
    $(document).click(function (evt) {
        $("#autocomplete").slideUp();
    });
    $("#autocomplete").css({
        top: ($("#searchinput").offset().top + $("#searchinput").outerHeight()) + "px",
        left: $("#searchinput").offset().left + "px"
    });
});

function replaceURLWithHyperlinks(text) {
    if (GexfJS.params.replaceUrls) {
        var _urlExp = /(\b(?:https?:\/\/)?[-A-Z0-9]+\.[-A-Z0-9.:]+(?:\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*)?)/ig,
            _protocolExp = /^https?:\/\//i,
            _res = text.split(_urlExp);
        return _res.map(function (_txt) {
            if (_txt.match(_urlExp)) {
                return $('<a>').attr({
                    href: (_protocolExp.test(_txt) ? '' : 'http://') + _txt,
                    target: "_blank"
                }).text(_txt.replace(_protocolExp, ''));
            } else {
                return $('<span>').text(_txt);
            }
        });
    }
    return $("<span>").text(text);
}

function hoverAC() {
    $("#autocomplete li").removeClass("hover");
    $("#liac_" + GexfJS.autoCompletePosition).addClass("hover");
    GexfJS.params.activeNode = GexfJS.graph.indexOfLabels.indexOf($("#liac_" + GexfJS.autoCompletePosition).text().toLowerCase());
}

function changePosAC(_n) {
    GexfJS.autoCompletePosition = _n;
    hoverAC();
}

function updateAutoComplete(_sender) {
    var _val = $(_sender).val().toLowerCase();
    var _ac = $("#autocomplete");
    var _acContent = $('<ul>');
    if (_val != GexfJS.lastAC || _ac.html() == "") {
        GexfJS.lastAC = _val;
        var _n = 0;
        GexfJS.graph.indexOfLabels.forEach(function (_l, i) {
            if (_n < 20 && _l.search(_val) != -1) {
                var closure_n = _n;
                $('<li>')
                    .attr("id", "liac_" + _n)
                    .append($('<a>')
                        .mouseover(function () {
                            changePosAC(closure_n);
                        })
                        .click(function () {
                            //displayNode(i, true);
                            highlight(i);
                            return false;
                        })
                        .text(GexfJS.graph.nodeList[i].name)
                    )
                    .appendTo(_acContent);
                _n++;
            }
        });
        GexfJS.autoCompletePosition = 0;
        _ac.html(
            $('<div>').append(
                $('<h4>').text("nodes")
                ).append(_acContent)
        );
    }
    hoverAC();
    _ac.show();
}