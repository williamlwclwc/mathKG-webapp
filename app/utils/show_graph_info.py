from app import mongo
def show_graph_info(user = None):
    graph_info = []
    if user is None:
        num_nodes = mongo.db.nodes.count()
        num_edges = mongo.db.edges.count()
    else:
        pass #check here
    
    num_nodes_info = "Number of Nodes: " + str(num_nodes)
    num_edges_info = "Number of Edges: " + str(num_edges)
    density_info = "Density of Graph: " + str(round(float(num_edges)/num_nodes/(num_nodes -1) , 5))
    graph_info.append(num_nodes_info)
    graph_info.append(num_edges_info)
    graph_info.append(density_info)

    return graph_info
