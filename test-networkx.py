import networkx as nx
from networkx.readwrite import gexf
from networkx.readwrite import json_graph
import json

# G = gexf.read_gexf("static/data/middle_school_extend.gexf")
# print(nx.info(G))
# G.add_node('test', modular=1, Degree=0, label='test')
# G.remove_node('test')
# print(G.nodes['Circle'])
# print(nx.info(G))
# G = gexf.write_gexf(G, "static/data/middle_school_extend.gexf")
# test_data = json_graph.node_link_data(G)
# with open("static/data/middle_school_extend.json", "w") as write_file:
#     json.dump(test_data, write_file)

with open("static/data/middle_school_extend.json", "r") as read_file:
    test_data = json.load(read_file)
G = json_graph.node_link_graph(test_data)
print(G.nodes['Circle'])