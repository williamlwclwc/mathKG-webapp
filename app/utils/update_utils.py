import networkx as nx
from app import mongo

# set degree and size
def update_degree_size(G, form2):
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

    # additional change implemented in nx graph
    if operation == 'add' or operation == 'edit':
        G.add_nodes_from([(new_node.pop('id'), new_node)])
    elif operation == 'delete':
        G.remove_node(form1.node_name.data)
