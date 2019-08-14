from app import app, login_manager, mongo
from .user import User
from networkx.readwrite import gexf, json_graph
import networkx as nx
import json
from flask import Flask, flash, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required, fresh_login_required
from .forms import node_form, edge_form, RegistrationForm
from app.utils.login_util import query_user
from app.utils.update_attr import update_attr
from shutil import copyfile
import logging


@app.route('/')
@app.route('/home')
def home():
    
    # provide a different graph for each user
    graphname = "app/static/data/graph_login_test"
    if current_user.get_id() != None:
        graphname += "_" + current_user.get_id() + ".json"
    else:
        graphname += ".json"

    # open graph json file: load into graph G
    with open(graphname, "r") as read_file:
            data = json.load(read_file)
    G = json_graph.node_link_graph(data)

    graph_info = []
    num_nodes = "Number of Nodes: " + str(G.number_of_nodes())
    num_edges = "Number of Edges: " + str(G.number_of_edges())
    density = "Density of Graph: " + str(round(nx.density(G), 5))
    graph_info.append(num_nodes)
    graph_info.append(num_edges)
    graph_info.append(density)

    return render_template('home.html', graph_info=graph_info, title="Home")

@app.route('/editGraph', methods=['get', 'post'])
def edit_graph():

    # provide a different graph for each user
    graphname = "app/static/data/graph_login_test"
    if current_user.get_id() != None:
        graphname += "_" + current_user.get_id() + ".json"
    else:
        graphname += ".json"

    form1 = node_form(request.form)
    form2 = edge_form(request.form)

    # open graph json file: load into graph G
    with open(graphname, "r") as read_file:
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
                flash(u"Add Failed: such node already exist", "danger")
            else:
                G.add_node(form1.node_name.data, 
                            category=form1.category.data, 
                            degree=0, viz={'size': 10}, 
                            # label=form1.node_name.data,
                            url=form1.url.data,
                            content=form1.content.data,
                            notes=form1.notes.data)
                print("added a node")
                flash(u"Added Node: " + "'" + form1.node_name.data + "'", 'success')
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
                flash(u"Updated Node: " + "'" + form1.node_name.data + "'", 'success')
            else:
                print("edit failed: such node does not exist")
                flash(u"Edit Failed: such node does not exist", "danger")

        # delete node
        if form1.delete_node.data and form1.validate():

            if G.has_node(form1.node_name.data):
                G.remove_node(form1.node_name.data)
                print("removed a node")
                flash(u"Removed Node: " + "'" + form1.node_name.data + "'", 'success')
            else:
                print("remove failed: such node does not exist")
                flash(u"Remove Failed: such node does not exist", "danger")
        # else:
        #     print(form1.validate())

        # add edge
        if form2.add_edge.data and form2.validate():
            
            if G.has_node(form2.source_name.data) and G.has_node(form2.target_name.data):
                G.add_edge(form2.source_name.data, form2.target_name.data, 
                relationship=form2.relationship.data, key=str(G.number_of_edges()),
                content=form2.content.data, notes=form2.notes.data)
                update_attr(G, form2)
                print("added an edge")
                flash(u"Added Edge (key: " + str(G.number_of_edges()) + "): " + "'" + form2.source_name.data + "' -> " 
                        + "'" + form2.target_name.data + "'" + 'success')
            else:
                print("add failed: source/target node does not exist")
                flash(u"Add Failed: source/target node does not exist", "danger")
        
        # edit edge
        if form2.edit_edge.data and form2.validate():
            if form2.key_num.data == "":
                print("you need to input the key of the edge")
                flash(u"Edit Failed: you need to input the key of the edge", "danger")
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
                flash(u"Updated Edge (key: " + str(G.number_of_edges()) + "): " + "'" + form2.source_name.data + "' -> " 
                      + "'" + form2.target_name.data + "'" + 'success')
            else:
                print("edit failed: such edge does not exist")
                flash(u"Edit Failed: such edge does not exist", "danger")

        # delete edge
        if form2.delete_edge.data and form2.validate():
            if form2.key_num.data == "":
                print("you need to input the key of the edge")
                flash(u"Edit Failed: you need to input the key of the edge", "danger")
            if G.has_edge(form2.source_name.data, form2.target_name.data, key=form2.key_num.data):
                G.remove_edge(form2.source_name.data, form2.target_name.data, key=form2.key_num.data)
                update_attr(G, form2)
                print("removed an edge")
                flash(u"Eemoved Edge (key: " + str(G.number_of_edges()) + "): " + "'" + form2.source_name.data + "' -> " 
                      + "'" + form2.target_name.data + "'" + 'success')
            else:
                print("remove failed: such edge does not exist")
                flash(u"Edit Failed: such edge does not exist", "danger")

        # save edited graph G into json file
        data = json_graph.node_link_data(G)
        with open(graphname, "w") as write_file:
            json.dump(data, write_file)
        return redirect(url_for('edit_graph'))
    return render_template('edit-graph.html', form_node=form1, form_edge=form2, 
                            graph_info=graph_info, title="Edit Graph")

@app.route('/about')
def authors():
    return render_template('about.html', title="About")

# 如果用户名存在则构建一个新的用户类对象，并使用用户名作为ID
# 如果不存在，必须返回None
@login_manager.user_loader
def load_user(username):
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id = username
        return curr_user
    # Must return None if username not found

# 从请求参数中获取Token，如果Token所对应的用户存在则构建一个新的用户类对象
# 并使用用户名作为ID，如果不存在，必须返回None
# @login_manager.request_loader
#     username = request.args.get('token')
#     user = query_user(username)
#     if user is not None:
#         curr_user = User()
#         curr_user.id = username
#         return curr_user
#     # Must return None if username not found

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/hello-test')
@login_required
def index():
    username = current_user.get_id()
    user = query_user(username)
    datapath = user['datapath']
    return render_template('hello-test.html',datapath=datapath)

@app.route('/home-test')
@fresh_login_required
def home_test():
    return 'Logged in as: %s' % current_user.get_id()

from app import mongo

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = query_user(username)
        # 验证表单中提交的用户名和密码
        if user is not None :
            user_auths = mongo.db.user_auths.find_one({'user_id':user['id']},{'_id':0})
            logging.info(user_auths)
            if request.form['password'] is None:
                flash('Password cannot be empty!')
            elif request.form['password'] == user_auths["credential"]:
                curr_user = User()
                curr_user.id = username

                # 通过Flask-Login的login_user方法登录用户
                login_user(curr_user, remember=True)

                # 如果请求中有next参数，则重定向到其指定的地址，
                # 没有next参数，则重定向到"index"视图
                next = request.args.get('next')
                return redirect(next or url_for('edit_graph'))
            else:
                flash('Wrong password!')
        else:
            flash('Invalid user name!')
    # GET 请求
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!' # 这里要加一个跳转

#register new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('edit_graph'))

    form = RegistrationForm(request.form)

    if request.method == 'POST':
        username = request.form.get('username')
        user = query_user(username)
        # 验证表单中提交的用户名和密码
        if user is not None:
            flash('you already register! please login.')
            return redirect(url_for('login'))
        if user is None:
            user = {}
            user['name'] = username
            user['id'] = mongo.db.users.find().count()
            user['email'] = ''
            user_auth = {}
            user_auth['id'] = mongo.db.user_auths.find().count()
            user_auth['user_id'] = user['id']
            user_auth['identifier'] = user['name']
            user_auth["identity_type"] = 'name'
            user_auth["credential"] = form.password.data
            mongo.db.users.insert_one(user)
            mongo.db.user_auths.insert_one(user_auth)
            # print(users)
            source = "app/static/data/graph_login_test.json"
            target = "app/static/data/graph_login_test_" + username + ".json"
            copyfile(source, target)
            logging.error(mongo.db.users.find({'name':username}))
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    # GET 请求
    return render_template('register.html', form_newuser=form)