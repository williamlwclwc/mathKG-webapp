# from app import mongo
import networkx as nx

def show_graph_info(G, timeline_date):
    graph_info = []
    num_nodes_info = "Number of Nodes: " + str(G.number_of_nodes())
    num_edges_info = "Number of Edges: " + str(G.number_of_edges())
    density_info = "Density of Graph: " + str(round(nx.density(G), 5))
    timeline_info = "Edition: " + timeline_date
    graph_info.append(num_nodes_info)
    graph_info.append(num_edges_info)
    graph_info.append(density_info)
    graph_info.append(timeline_info)
    # if user is None:
    #     num_nodes = mongo.db.nodes.count()
    #     num_edges = mongo.db.edges.count()
    # else:
    #     pass #check here
    
    return graph_info





    
