from flask import Flask
from flask import render_template, redirect, url_for, request
import networkx as nx
from networkx.readwrite import gexf
from networkx.readwrite import json_graph
import json
import logging
from wtforms import Form, TextField, TextAreaField, IntegerField, SubmitField, SelectField, validators


app = Flask(__name__)


class node_form(Form):
    node_name = TextField("node_name", [validators.InputRequired()])
    category = IntegerField("category", [validators.Optional()])
    url = TextField("url", [validators.Optional()])
    content = TextAreaField("content", [validators.Optional()])
    notes = TextAreaField("notes", [validators.Optional()])
    add_node = SubmitField("Add Node")
    edit_node = SubmitField("Edit Node")
    delete_node = SubmitField("Delete Node")


class edge_form(Form):
    key_num = TextField("key_num", [validators.Optional()])
    source_name = TextField("source_name", [validators.InputRequired()])
    target_name = TextField("target_name", [validators.InputRequired()])
    relationship = SelectField(
        "relationship", validators=[validators.Optional()],
        choices=[("", ""), ("contain", "contain"), ("arithmetic operation", "arithmetic operation"),
        ("property", "property"), ("algorithm", "algorithm"), ("application", "application"), 
        ("example", "example"), ("expression", "expression"), ("theorem", "theorem"), 
        ("conjecture", "conjecture"), ("proof", "proof"), ("proof methods", "proof methods"),
        ("corollary", "corollary"), ("formula", "formula")])
    content = TextAreaField("content", [validators.Optional()])
    notes = TextAreaField("notes", [validators.Optional()])
    add_edge = SubmitField("Add Edge")
    edit_edge = SubmitField("Edit Edge")
    delete_edge = SubmitField("Delete Edge")


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
    attrs = {form2.source_name.data: {'Degree': degree_source, 'viz': {'size': size_source}}, 
            form2.target_name.data: {'Degree': degree_target, 'viz': {'size': size_target}}}
    nx.set_node_attributes(G, attrs)


@app.route('/')
@app.route('/editGraph', methods=['get', 'post'])


def edit_graph():
    form1 = node_form(request.form)
    form2 = edge_form(request.form)

    # open graph json file: load into graph G
    with open("static/data/middle_school_3.json", "r") as read_file:
            data = json.load(read_file)
    G = json_graph.node_link_graph(data)

    graph_info = []
    num_nodes = "Number of Nodes: " + str(G.number_of_nodes())
    num_edges = "Number of Edges: " + str(G.number_of_edges())
    density = "Density of Graph: " + str(round(nx.density(G), 5))
    graph_info.append(num_nodes)
    graph_info.append(num_edges)
    graph_info.append(density)

    if request.method == 'POST':

        # add node
        if form1.add_node.data and form1.validate():

            if G.has_node(form1.node_name.data):
                print("add failed: such node already exist")
            else:
                G.add_node(form1.node_name.data, 
                            category=form1.category.data, 
                            degree=0, viz={'size': 10}, 
                            # label=form1.node_name.data,
                            url=form1.url.data,
                            content=form1.content.data,
                            notes=form1.notes.data)
                print("added a node")
        # else:
        #     print(form1.validate())
        
        # edit node
        if form1.edit_node.data and form1.validate():
            if G.has_node(form1.node_name.data):
                attrs = {}
                if form1.category.data != "":
                    attrs.update({"category": form1.category.data})
                if form1.url.data != "":
                    attrs.update({"url": form1.url.data})
                if form1.content.data != "":
                    attrs.update({"content": form1.content.data})
                if form1.notes.data != "":
                    attrs.update({"notes": form1.notes.data})
                attr = {form1.node_name.data: attrs} 
                nx.set_node_attributes(G, attr)
                print("updated a node")
            else:
                print("edit failed: such node does not exist")

        # delete node
        if form1.delete_node.data and form1.validate():

            if G.has_node(form1.node_name.data):
                G.remove_node(form1.node_name.data)
                print("removed a node")
            else:
                print("remove failed: such node does not exist")
        # else:
        #     print(form1.validate())

        # add edge
        if form2.add_edge.data and form2.validate():
            
            G.add_edge(form2.source_name.data, form2.target_name.data, 
            relationship=form2.relationship.data, key=str(G.number_of_edges()),
            content=form2.content.data, notes=form2.notes.data)
            update_attr(G, form2)
            print("added an edge")
        
        # edit edge
        if form2.edit_edge.data and form2.validate():
            if form2.key_num.data == "":
                print("you need to input the key of the edge")
            elif G.has_edge(form2.source_name.data, form2.target_name.data, key=form2.key_num.data):
                attrs = {}
                if form2.relationship.data != "":
                    attrs.update({"relationship": form2.relationship.data})
                if form2.content.data != "":
                    attrs.update({"content": form2.content.data})
                if form2.notes.data != "":
                    attrs.update({"notes": form2.notes.data})
                attr = {(form2.source_name.data, form2.target_name.data, form2.key_num.data): attrs} 
                nx.set_edge_attributes(G, attr)
                print("updated an edge")
            else:
                print("edit failed: such edge does not exist")

        # delete edge
        if form2.delete_edge.data and form2.validate():
            if form2.key_num.data == "":
                print("you need to input the key of the edge")
            if G.has_edge(form2.source_name.data, form2.target_name.data, key=form2.key_num.data):
                G.remove_edge(form2.source_name.data, form2.target_name.data, key=form2.key_num.data)
                update_attr(G, form2)
                print("deleted an edge")

            else:
                print("remove failed: such edge does not exist")

        # save edited graph G into json file
        data = json_graph.node_link_data(G)
        with open("static/data/middle_school_3.json", "w") as write_file:
            json.dump(data, write_file)
        return redirect(url_for('edit_graph'))
    return render_template('echart-demo.html', form_node=form1, form_edge=form2, graph_info=graph_info)

if __name__ == '__main__':
    app.run(debug=True, host='10.110.165.244', port=5000)
    # app.run(debug=True)