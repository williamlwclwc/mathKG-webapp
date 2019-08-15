# users = [
#     {'username': 'Tom', 'password': '111111'},
#     {'username': 'Michael', 'password': '123456'},
#     {'username': 'xlitong', 'password':'111111'}
# ]
from app import mongo
from flask import  flash
from networkx.readwrite import json_graph
import networkx as nx
import json

# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(username):
    user = mongo.db.users.find_one({'name':username},{'_id':0})
    if user is not None:
        return user
    else:
        return None

def basic_graph_update():
    # firstly update basic graph
    basic_graph_name = "app/static/data/graph_login_test"
    raw_graph_name = "app/static/rawdata/graph_login_test.json"
    # open graph json file: load into graph G
    with open(basic_graph_name + '.json', "r") as basic_graph_file:
            basic_graph_data = json.load(basic_graph_file)
    basic_graph = json_graph.node_link_graph(basic_graph_data)
    node_num = nx.number_of_nodes(basic_graph)
    edge_num = nx.number_of_edges(basic_graph)
    if node_num != mongo.db.nodes.count() or edge_num != mongo.db.edges.count():
        edges = list()
        for item in mongo.db.edges.find({},{'_id':0}):
            edges.append(item)
        nodes = list()
        for item in mongo.db.nodes.find({},{'_id':0}):
            nodes.append(item)
        graph = {}
        graph['directed'] = True
        graph["multigraph"] = True
        graph['graph'] = {"node_default": {"Out-Degree": 0, "In-Degree": 0}, "edge_default": {}, "mode": "static"}
        graph['nodes'] = nodes
        graph['links'] = edges
        with open(raw_graph_name ,'w') as raw_graph_file:
            raw_graph_file.write(json.dumps(graph))
    cal_degree_size(raw_graph_name, basic_graph_name + '.json')

def cal_degree_size(input_file, output_file):
    # open graph json file: load into graph G
    with open(input_file, "r") as read_file:
        data = json.load(read_file)
    G = json_graph.node_link_graph(data)

    list_degree = [d for n, d in G.degree()]
    degree_max = max(list_degree)
    degree_min = min(list_degree)

    max_size = 30
    min_size = 10

    attrs = {}
    for node_name, degree in G.degree():
        attr = {}
        size = (degree - degree_min) * (max_size-min_size) / (degree_max-degree_min) + min_size
        attr = {node_name: {'degree': degree, 'viz': {'size': size}}}
        attrs.update(attr)

    nx.set_node_attributes(G, attrs)

    attrs = {}
    for source, target, key in G.edges(keys=True):
        attr = {}
        source_size = nx.get_node_attributes(G, 'viz')
        source_size = source_size[source]
        source_size = source_size['size']
        target_size = nx.get_node_attributes(G, 'viz')
        target_size = target_size[target]
        target_size = target_size['size']
        weight = int(source_size + target_size)
        weight *= 10
        attr = {(source, target, key): {'value': weight}}
        attrs.update(attr)

    nx.set_edge_attributes(G, attrs)

    data = json_graph.node_link_data(G)
    with open(output_file, "w") as write_file:
        json.dump(data, write_file)