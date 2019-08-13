import networkx as nx

# set degree and size
def update_attr(G, form2):
    # calculate new degree and size, max_size = 30, min_size = 10
    list_degree = [d for n, d in G.degree()]
    degree_max = max(list_degree)
    degree_min = min(list_degree)
    degree_source = G.degree(nbunch=form2.source_name.data)
    degree_target = G.degree(nbunch=form2.target_name.data)
    if degree_source >= degree_max:
        size_source = 30
    else:
        size_source = (degree_source - degree_min) * (30-10) / (degree_max-degree_min) + 10
    if degree_target >= degree_max:
        size_target = 30
    else:
        size_target = (degree_target - degree_min) * (30-10) / (degree_max-degree_min) + 10
    attrs = {form2.source_name.data: {'degree': degree_source, 'viz': {'size': size_source}}, 
            form2.target_name.data: {'degree': degree_target, 'viz': {'size': size_target}}}
    nx.set_node_attributes(G, attrs)