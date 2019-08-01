from flask import Flask
from flask import render_template, redirect, url_for, request
import networkx as nx
from networkx.readwrite import gexf
from networkx.readwrite import json_graph
import json
from wtforms import Form, TextField, IntegerField, SubmitField, validators


app = Flask(__name__)


class add_node_form(Form):
    node_name = TextField("node_name", [validators.DataRequired()])
    category = IntegerField("category", [validators.DataRequired()])
    label = TextField("label")
    submit1 = SubmitField("Add Node")


class delete_node_form(Form):
    node_name = TextField("node_name", [validators.DataRequired()])
    submit2 = SubmitField("Delete Node")


class add_edge_form(Form):
    source_name = TextField("source_name", [validators.DataRequired()])
    target_name = TextField("target_name", [validators.DataRequired()])
    relationship = TextField("relation", [validators.DataRequired()])
    submit3 = SubmitField("Add Edge")


class delete_edge_form(Form):
    source_name = TextField("source_name", [validators.DataRequired()])
    target_name = TextField("target_name", [validators.DataRequired()])
    submit4 = SubmitField("Delete Edge")


@app.route('/')
@app.route('/editGraph', methods=['get', 'post'])


def edit_graph():
    form1 = add_node_form(request.form)
    form2 = delete_node_form(request.form)
    form3 = add_edge_form(request.form)
    form4 = delete_edge_form(request.form)

    if request.method == 'POST':
        with open("static/data/middle_school_extend.json", "r") as read_file:
                data = json.load(read_file)
        G = json_graph.node_link_graph(data)

        if form1.submit1.data and form1.validate():
            if form1.label.data == "":
                label_name = form1.node_name.data
            else:
                label_name = form1.label.data

            G.add_node(form1.node_name.data, 
                        modular=form1.category.data, 
                        Degree=0, viz={'size': 50}, 
                        label=label_name)
        
        if form2.submit2.data and form2.validate():
            G.remove_node(form2.node_name.data)

        if form3.submit3.data and form3.validate():
            G.add_edge(form3.source_name.data, form3.target_name.data, relationship=form3.relationship.data)

        if form4.submit4.data and form4.validate():
            G.remove_edge(form4.source_name.data, form4.target_name.data)

        data = json_graph.node_link_data(G)
        with open("static/data/middle_school_extend.json", "w") as write_file:
            json.dump(data, write_file)
        return redirect(url_for('edit_graph'))
    return render_template('echart-demo.html', 
            form_add_node=form1, form_delete_node=form2, 
            form_add_edge=form3, form_delete_edge=form4)

if __name__ == '__main__':
    app.run(debug=True, host='10.110.165.244', port=5000)
    # app.run(debug=True)