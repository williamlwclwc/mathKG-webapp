# users = [
#     {'username': 'Tom', 'password': '111111'},
#     {'username': 'Michael', 'password': '123456'},
#     {'username': 'xlitong', 'password':'111111'}
# ]


# 需要定义的常量：basic graph名称， data 路径， raw data 路径， 

from app import mongo
from flask import  flash
from networkx.readwrite import json_graph
import networkx as nx
import json
import datetime
import logging

raw_graph_name = "app/static/rawdata/graph_login_test.json"

# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(username):
    user = mongo.db.users.find_one({'name':username},{'_id':0})
    if user is not None:
        return user
    else:
        return None

# 先生成未计算节点大小的 "app/static/rawdata/graph_login_test.json"
# 生成计算了节点大小的basic graph 
# 返回 raw_graph_name
def basic_graph_update():
    # firstly update basic graph
    basic_graph_name = "app/static/data/graph_login_test"
    
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
    return raw_graph_name

# check here: the size in history editions may be wrong
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

# 所有的用户修改，对新点/边 只有add
# 对原图（即数据库中的点和边）只有edit 和 delete,
# 原图 先删后加 记为edit
# 其实好像不需要这么麻烦
# 取得time_str 之前所有用户的改动，并写入文件 "app/static/data/" + user['name'] + '_' + time_str + '_' + 'change.json'
# 返回 time_str, imported_nodes, imported_edges (id/key), user_change_name
def get_user_changes(user, time_str = None):

    # 默认得到所有的更改，即显示明天以前的所有修改
    if time_str == None:
        time_structured = datetime.date.today() + datetime.timedelta(days=1)
        time_str = time_structured.strftime("%Y-%m-%d")

    if user.__contains__('changes') and len(user['changes']) > 0:
        user['changes'].sort(reverse=True) # changes的 id大小关系 和 时间戳大小关系 一致

        edges = list()
        nodes = list()
        imported_nodes = list()
        imported_edges = list()
        for change_id in user['changes']:
            change = mongo.db.user_changes.find_one({'id':change_id},{'_id':0})
            if change['timestamp'] < time_str:
                if (change['type'] == 'edge') and (change['content']['key'] not in imported_edges):
                    edges.append(change['content'])
                    imported_edges.append(change['content']['key'])
                elif (change['type'] == 'node') and (change['content']['id'] not in imported_nodes):
                    nodes.append(change['content'])
                    imported_nodes.append(change['content']['id'])

        if len(imported_edges) or len(imported_nodes):
            user_change_name = "app/static/rawdata/" + user['name'] + '_' + time_str + '_' + 'change.json'
            #写入到一个单独的json文件中
            graph = {}
            graph['nodes'] = nodes
            graph['links'] = edges
            with open(user_change_name ,'w') as change_graph_file:
                change_graph_file.write(json.dumps(graph))
            return time_str, imported_nodes, imported_edges, user_change_name
    
    return None

# 可以直接用nx.add_nodes_from 来更新数据
# 生成"app/static/rawdata/" + user['name'] + '_' + time_str + '_' + 'merged.json' 文件
# 返回 merged_name
def merge_user_changes(user, time_str, imported_nodes, imported_edges):

    # open graph json file: load into graph G
    with open(raw_graph_name, "r") as raw_graph_file:
        raw_graph_data = json.load(raw_graph_file)
    G = json_graph.node_link_graph(raw_graph_data)

    user_change_name = "app/static/rawdata/" + user['name'] + '_' + time_str + '_' + 'change.json'
    with open(user_change_name, "r") as user_change_file:
        user_change_data = json.load(user_change_file)
    user_change_graph = json_graph.node_link_graph(user_change_data)

    # nodes = ((id, attr) for id,attr in G.nodes(data=True) if id in imported_nodes)
    raw_nodes = [ id for id in G.nodes() if id in imported_nodes]
    # new_nodes = [id for id in imported_nodes if id not in raw_nodes]
    # edges = ((source, target, key, attr) for source, target, key, attr in G.edges(data=True, keys=True) if key in imported_edges)
    raw_edges = [key for source, target, key in G.edges(keys=True) if key in imported_edges]
    # new_edges = [key for key in imported_edges if key not in raw_edges]

    all_node_edit = []
    all_node_delete = []
    # [(id, data) for id,data in user_change_graph.nodes(data=True) if ((id in raw_nodes) and (data['operation'] in ['add', 'edit']))]
    for id, data in user_change_graph.nodes(data=True):
        if data['operation'] in ['add', 'edit']:
            data.pop('operation')
            all_node_edit.append((id,data))
        elif (id in raw_nodes):
            all_node_delete.append(id)

    all_edge_edit = []
    all_edge_delete = []
    for source, target, key, attr in user_change_graph.edges(data=True, keys=True):
        if attr['operation'] in ['add', 'edit']:
            attr.pop('operation')
            all_edge_edit.append((source, target, key, attr))
        elif (id in raw_edges):
            all_edge_delete.append((source, target, key))

    G.add_nodes_from(all_node_edit)
    G.remove_nodes_from(all_node_delete)
    G.add_edges_from(all_edge_edit)
    G.remove_edges_from(all_edge_delete)

    merged_name = "app/static/rawdata/" + user['name'] + '_' + time_str + '_' + 'merged.json'
    data = json_graph.node_link_data(G)

    with open(merged_name, "w") as write_file:
        json.dump(data, write_file)
    return merged_name

def get_edition_by_date(user, time_str = None):
    
    raw_graph_name = basic_graph_update()

    # 默认得到所有的更改，即显示明天以前的所有修改
    if time_str == None:
        time_structured = datetime.date.today() + datetime.timedelta(days=1)
        time_str = time_structured.strftime("%Y-%m-%d")


    user_change = get_user_changes(user, time_str)


    user_graph_name = "app/static/data/graph_login_test" + '_' + user['name'] + '_' + time_str + '.json'
    if user_change is not None:
        merged_name = merge_user_changes(user, user_change[0], user_change[1], user_change[2])
        cal_degree_size(merged_name, user_graph_name)
    else:
        cal_degree_size(raw_graph_name, user_graph_name)
