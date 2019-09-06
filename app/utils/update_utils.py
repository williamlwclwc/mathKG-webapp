import networkx as nx
from app import mongo

# set degree and size for a number of nodes
def update_degree_size(G, *node_ids):

    # calculate new degree and size, max_size = 30, min_size = 10
    list_degree = [d for n, d in G.degree()]
    degree_max = max(list_degree)
    degree_min = min(list_degree)

    for node_id in node_ids:
        degree_node = G.degree(nbunch=node_id)
        if degree_node >= degree_max:
            size_node = 30
        else:
            size_node = (degree_node - degree_min) * (30-10) / (degree_max-degree_min) + 10

        attrs = {node_id: {'degree': degree_node, 'viz': {'size': size_node}}}
        nx.set_node_attributes(G, attrs)

# return none
def update_node(G, form1, user_name, operation, now_str):

    # record new node change in mongodb
    new_node = {}
    new_node['category'] = form1.category.data
    new_node['wiki_url'] = form1.wiki_url.data
    new_node['content'] = form1.content.data
    new_node['note'] = form1.notes.data
    new_node['id'] = form1.node_name.data
    new_node['operation'] = operation
    new_change = {}
    new_change['type'] = 'node'
    new_change['content'] = new_node
    new_change['timestamp'] = now_str

    # edit 时要补全信息
    if operation == 'edit':
        original_node_data = G.nodes[new_node['id']]
        if form1.category.data == "":
            new_node['category'] = original_node_data['category']
        if form1.wiki_url.data == "":
            new_node['wiki_url'] = original_node_data['wiki_url']
        if form1.content.data == "":
            new_node['content'] = original_node_data['content']
        if form1.notes.data == "":
            new_node['note'] = original_node_data['note']


    if "user_changes" in mongo.db.list_collection_names():
        new_change['id'] = mongo.db.user_changes.count()
    else:
        new_change['id'] = 0
    mongo.db.user_changes.insert_one(new_change)
    
    user_profile = mongo.db.users.find_one({'name' : user_name }, {'_id': 0})
    if user_profile.__contains__('changes'):
        user_profile['changes'].append(new_change['id'])
        mongo.db.users.update({'name': user_name},{'$set': {'changes': user_profile['changes']}})
    else:
        mongo.db.users.update({'name': user_name},{'$set': {'changes': [new_change['id']]}})

    # additional configuration not recorded in mongodb
    new_node['degree'] = 0
    new_node['viz'] = {'size': 10}

    # additional change implemented in nx multidigraph
    if operation == 'add' or operation == 'edit':
        G.add_nodes_from([(new_node.pop('id'), new_node)])
    elif operation == 'delete':
        G.remove_node(form1.node_name.data)

# return key
def update_edge(G, form2, user_name, operation, now_str):

    # record new edge change in mongodb
    new_edge = {}
    new_edge['source'] = form2.source_name.data
    new_edge['target'] = form2.target_name.data
    new_edge['relationship'] = form2.relationship.data
    new_edge['note'] = form2.notes.data
    new_edge['content'] = form2.content.data
    new_edge['key'] = str(form2.key_num.data)
    new_edge['operation'] = operation
    new_change = {}
    new_change['type'] = 'edge'
    new_change['timestamp'] = now_str  

    # edit 时要补全信息
    if operation == 'edit':
        original_edge_data = G.edges[new_edge['source'], new_edge['target'], new_edge['key']]
        if form2.relationship.data == "":
            new_edge['relationship'] = original_edge_data['relationship']
        if form2.notes.data == "":
            new_edge['note'] = original_edge_data['note']
        if form2.content.data == "":
            new_edge['content'] = original_edge_data['content']

    if "user_changes" in mongo.db.list_collection_names():
        new_change['id'] = mongo.db.user_changes.count()
    else:
        new_change['id'] = 0
    
    
    # add 时要忽略 输入的key 之后才能插入 new_change
    if operation == 'add':
        new_edge['key'] = 'new_change_' + str(new_change['id'])
    new_change['content'] = new_edge
    mongo.db.user_changes.insert_one(new_change)

    user_profile = mongo.db.users.find_one({'name' : user_name }, {'_id': 0})
    if user_profile.__contains__('changes'):
        user_profile['changes'].append(new_change['id'])
        mongo.db.users.update({'name': user_name},{'$set': {'changes': user_profile['changes']}})
    else:
        mongo.db.users.update({'name': user_name},{'$set': {'changes': [new_change['id']]}})

    # additional change implemented in nx multidigraph
    edge_key = new_edge.pop('key')
    if operation == 'add' or operation == 'edit':
        G.add_edges_from([(new_edge.pop('source'),new_edge.pop('target'), edge_key, new_edge)])
    elif operation == 'delete':
        G.remove_edge(new_edge['source'], new_edge['target'], key = new_edge['key'])
    if operation != 'edit':
        update_degree_size(G, form2.source_name.data, form2.target_name.data)
    return edge_key