from flask import Flask
from flask import render_template, redirect, url_for, request
import networkx as nx
from networkx.readwrite import gexf
from networkx.readwrite import json_graph
import json
import logging
from wtforms import Form, TextField, IntegerField, SubmitField, validators


app = Flask(__name__)


class node_form(Form):
    node_name = TextField("node_name", [validators.InputRequired()])
    category = IntegerField("category", [validators.Optional()])
    content = TextField("content", [validators.Optional()])
    notes = TextField("notes", [validators.Optional()])
    add_node = SubmitField("Add Node")
    edit_node = SubmitField("Edit Node")
    delete_node = SubmitField("Delete Node")


class edge_form(Form):
    source_name = TextField("source_name", [validators.InputRequired()])
    target_name = TextField("target_name", [validators.InputRequired()])
    relationship = TextField("relation", [validators.Optional()])
    notes = TextField("notes", [validators.Optional()])
    add_edge = SubmitField("Add Edge")
    edit_edge = SubmitField("Edit Edge")
    delete_edge = SubmitField("Delete Edge")


@app.route('/')
@app.route('/editGraph', methods=['get', 'post'])


def edit_graph():
    form1 = node_form(request.form)
    form2 = edge_form(request.form)

    if request.method == 'POST':
        # open graph json file: load into graph G
        with open("static/data/middle_school_extend.json", "r") as read_file:
                data = json.load(read_file)
        G = json_graph.node_link_graph(data)

        # add node
        if form1.add_node.data and form1.validate():

            if G.has_node(form1.node_name.data):
                print("add failed: this node already exist")
            else:
                G.add_node(form1.node_name.data, 
                            modular=form1.category.data, 
                            Degree=0, viz={'size': 50}, 
                            label=form1.node_name.data)
                print("added a node")
        # else:
        #     print(form1.validate())
        
        # delete node
        if form1.delete_node.data and form1.validate():

            if G.has_node(form1.node_name.data):
                G.remove_node(form1.node_name.data)
                print("removed a node")
            else:
                print("remove failed: this node does not exist")
        # else:
        #     print(form1.validate())

        # add edge
        if form2.add_edge.data and form2.validate():

            G.add_edge(form2.source_name.data, form2.target_name.data, relationship=form2.relationship.data)
            print("added an edge")
        
        # delete edge
        if form2.delete_edge.data and form2.validate():
            
            if G.has_edge(form2.source_name.data, form2.target_name.data):
                G.remove_edge(form2.source_name.data, form2.target_name.data)
                print("deleted an edge")
            else:
                print("remove failed: this edge does not exist")

        # save edited graph G into json file
        data = json_graph.node_link_data(G)
        with open("static/data/middle_school_extend.json", "w") as write_file:
            json.dump(data, write_file)
        return redirect(url_for('edit_graph'))
    return render_template('echart-demo.html', form_node=form1, form_edge=form2)

if __name__ == '__main__':
    app.run(debug=True, host='10.110.165.244', port=5000)
    # app.run(debug=True)