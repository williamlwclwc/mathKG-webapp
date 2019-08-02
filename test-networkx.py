import networkx as nx
from networkx.readwrite import gexf
from networkx.readwrite import json_graph
import json

# G = gexf.read_gexf("static/data/middle_school_extend.gexf")
with open("static/data/middle_school_extend.json", "r") as read_file:
    data = json.load(read_file)
G = json_graph.node_link_graph(data)
print(nx.info(G))
# G.add_node('test1', modular=1, Degree=0, viz={'size': 50}, label='test1')
# G.remove_node('test')
# print(G.nodes['Circle'])
# print(G.nodes['test1'])
degree_max = max([d for n, d in G.degree()])
print(degree_max)

print("circle: ", nx.degree(G, nbunch='Circle'))
print(nx.info(G))
# G = gexf.write_gexf(G, "static/data/middle_school_extend.gexf")
# data = json_graph.node_link_data(G)
# with open("static/data/middle_school_extend.json", "w") as write_file:
#     json.dump(data, write_file)