import networkx as nx
import json
from networkx.readwrite import json_graph


input_file = "static/rawdata/graph_from_mongodb.json"
output_file = "static/data/graph_from_mongodb.json"

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

data = json_graph.node_link_data(G)
with open(output_file, "w") as write_file:
    json.dump(data, write_file)


