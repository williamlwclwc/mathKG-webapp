var filename = 'static/data/';
var username = document.getElementById("user profile");
if(username!=null) {
    filename += 'graph_login_test' + '_' + username.innerHTML + '.json';
} else {
    filename += 'graph_login_test.json';
}
console.log(filename);

// a dictionary define color of the nodes
var node_color = {
    "0": "#f30909",
    "1": "#1d52ce" 
}
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

const Graph = ForceGraph3D()
      (document.getElementById('3d-graph'))
        .jsonUrl(filename +'?timestamp='+ new Date().getTime())
        .nodeLabel('id')
        .nodeColor(node => {
            return node_color[node.category];
        })
        .linkColor(link => {
            return link_color[link.relationship];
        })
        .linkWidth(1)
        // .linkCurvature(10)
        .linkOpacity(1);
