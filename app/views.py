from app import app, login_manager, mongo
from .user import User
from networkx.readwrite import json_graph
import networkx as nx
import json
from flask import Flask, flash, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required, fresh_login_required
from .forms import node_form, edge_form, RegistrationForm
from app.utils.login_utils import query_user, basic_graph_update, cal_degree_size, get_user_changes, merge_user_changes, get_edition_by_date
from app.utils.update_utils import update_degree_size, update_node, update_edge
from app.utils.show_graph_info import show_graph_info
from app.utils.logout_utils import del_user_file
from shutil import copyfile
import logging
import datetime


@app.route('/')
@app.route('/home')
def home():
    # # provide a different graph for each user
    # graphname = "app/static/data/graph_login_test"
    # user_name = current_user.get_id()
    # if user_name != None:
    #     graphname += "_" + user_name + ".json"
    #     # graph_info = show_graph_info(user_name)
    #     graph_info = show_graph_info() # check here
    # else:
    #     graphname += ".json"
    #     graph_info = show_graph_info()

    # return render_template('home.html', graph_info=graph_info, title="Home")
    return render_template('home.html', title="Home")

@app.route('/editGraph', methods=['get', 'post'])
def edit_graph():

    slider_num = request.args.get('slider_num')
    timeline_date = request.args.get('timeline_date')
    if slider_num == None:
        slider_num = '5'
    # check here 时间可以简化
    time_structured = datetime.date.today() + datetime.timedelta(days=1)
    time_str = time_structured.strftime("%Y-%m-%d")
    
    if timeline_date == None:

        timeline_date = time_str

    # provide a different graph for each user
    graphname = "app/static/data/graph_login_test"
    
    authorized = 0 # 未登录不能修改
    user_name = current_user.get_id()
    user = query_user(user_name)
    if user_name != None:
        authorized = 1
        graphname += '_' + user_name + '_' + timeline_date + '.json'
    else:
        graphname += ".json"

    form1 = node_form(request.form)
    form2 = edge_form(request.form)

    # open graph json file: load into graph G
    with open(graphname, "r") as user_file:
            user_graph = json.load(user_file)
    G = json_graph.node_link_graph(user_graph) # check here
    graph_info = show_graph_info(G, timeline_date)

    if request.method == 'POST':
        # record timestamp
        now_structured = datetime.datetime.now()
        now_str = now_structured.strftime("%Y-%m-%d %H:%M:%S")
        # now_structured = time.localtime()
        # now_str = time.strftime("%Y-%m-%d %H:%M:%S", now_structured)

        # add node
        if form1.add_node.data and form1.validate():

            if G.has_node(form1.node_name.data):
                flash(u"Add Failed: such node already exist", "danger")
            else:
                update_node(G, form1, user_name, 'add', now_str)
                flash(u"Added Node: " + "'" + form1.node_name.data + "'", 'success')
        
        # edit node
        if form1.edit_node.data and form1.validate():

            if G.has_node(form1.node_name.data):
                update_node(G, form1, user_name, 'edit', now_str)
                flash(u"Updated Node: " + "'" + form1.node_name.data + "'", 'success')
            else:
                flash(u"Edit Failed: such node does not exist", "danger")

        # delete node
        if form1.delete_node.data and form1.validate():

            if G.has_node(form1.node_name.data):
                update_node(G, form1, user_name, 'delete', now_str)
                flash(u"Removed Node: " + "'" + form1.node_name.data + "'", 'success')
            else:
                flash(u"Remove Failed: such node does not exist", "danger")

        # add edge
        if form2.add_edge.data and form2.validate():
            
            if G.has_node(form2.source_name.data) and G.has_node(form2.target_name.data):
                edge_key = update_edge(G, form2, user_name, 'add', now_str)
                flash(u"Added Edge (key: " + edge_key + "): " + "'" + form2.source_name.data + "' -> " 
                        + "'" + form2.target_name.data + "'" + 'success')
            else:
                flash(u"Add Failed: source/target node does not exist", "danger")
        
        # edit edge
        if form2.edit_edge.data and form2.validate():
            if form2.key_num.data == "":
                flash(u"Edit Failed: you need to input the key of the edge", "danger")
            elif G.has_edge(form2.source_name.data, form2.target_name.data, key=form2.key_num.data):
                edge_key = update_edge(G, form2, user_name, 'edit', now_str)
                flash(u"Updated Edge (key: " + edge_key + "): " + "'" + form2.source_name.data + "' -> " 
                      + "'" + form2.target_name.data + "'" + 'success')
            else:
                flash(u"Edit Failed: such edge does not exist", "danger")

        # delete edge
        if form2.delete_edge.data and form2.validate():
            if form2.key_num.data == "":
                flash(u"Edit Failed: you need to input the key of the edge", "danger")
            if G.has_edge(form2.source_name.data, form2.target_name.data, key=form2.key_num.data):
                edge_key = update_edge(G, form2, user_name, 'delete', now_str)
                flash(u"Eemoved Edge (key: " + edge_key + "): " + "'" + form2.source_name.data + "' -> " 
                      + "'" + form2.target_name.data + "'" + 'success')
            else:
                flash(u"Edit Failed: such edge does not exist", "danger")

        # save edited graph G into json file
        with open(graphname, "w") as user_file:
            data = json_graph.node_link_data(G)
            json.dump(data, user_file)

        # timeline
        if request.form.__contains__('timeline_submit') and request.form['timeline_submit'] == 'Go To':
            
            print((request.form))
            timeline_date = request.form['timeline_date']
            slider_num = request.form['timeline_slider']

            get_edition_by_date(user, timeline_date)


        return redirect(url_for('edit_graph', slider_num = slider_num, timeline_date =  timeline_date))
        # return redirect(url_for('index', slider_num = slider_num ))

    graphname4js = graphname.split('/', 1)[1] # javacript 读取json文件时路径没有app/
    print(slider_num)
    return render_template('edit-graph.html', form_node=form1, form_edge=form2, 
                            graph_info=graph_info, authorized = authorized, graphname4js = graphname4js, slider_num = slider_num, title="Edit Graph")

@app.route('/index', methods=['post','get'])  #这里指定了接收的username的类型,如果不符合会报错,
def index():                     #可以将string改成path, 这样username就会被当成路径来接收,也就是说username可以是任意可键入路由的值了
    slider_num = request.args.get('slider_num')
    if slider_num == None:
        slider_num = 5
    return str(slider_num)




@app.route('/3dlayout')
def threeD():
    # check here 时间可以简化
    time_structured = datetime.date.today() + datetime.timedelta(days=1)
    time_str = time_structured.strftime("%Y-%m-%d")

    # provide a different graph for each user
    graphname = "app/static/data/graph_login_test"

    user_name = current_user.get_id()
    if user_name != None:
        graphname += '_' + user_name + '_' + time_str + '.json'
    else:
        graphname += ".json"
    graphname4js = graphname.split('/', 1)[1] # javacript 读取json文件时路径没有app/

    return render_template('3D_layout.html', graphname4js = graphname4js, title="3D")

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

# @app.route('/hello-test')
# @login_required
# def index():
#     username = current_user.get_id()
#     user = query_user(username)
#     datapath = user['datapath']
#     return render_template('hello-test.html',datapath=datapath)

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
                flash(u'Password cannot be empty!', 'danger')
            elif request.form['password'] == user_auths["credential"]:
                curr_user = User()
                curr_user.id = username

                # 通过Flask-Login的login_user方法登录用户
                login_user(curr_user, remember=True)

                # 后台更新数据
                get_edition_by_date(user)
                # raw_graph_name = basic_graph_update()
                # user_change = get_user_changes(user)

                # # check here 时间可以简化
                # time_structured = datetime.date.today() + datetime.timedelta(days=1)
                # time_str = time_structured.strftime("%Y-%m-%d")

                # user_graph_name = "app/static/data/graph_login_test" + '_' + user['name'] + '_' + time_str + '.json'
                # if user_change is not None:
                #     merged_name = merge_user_changes(user, user_change[0], user_change[1], user_change[2])
                #     cal_degree_size(merged_name, user_graph_name)
                # else:
                #     cal_degree_size(raw_graph_name, user_graph_name)

                # 如果请求中有next参数，则重定向到其指定的地址，
                # 没有next参数，则重定向到"index"视图
                next = request.args.get('next')
                return redirect(next or url_for('edit_graph'))
            else:
                flash(u'Wrong password!', 'danger')
        else:
            flash(u'Invalid user name!', 'danger')
    # GET 请求
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    user_name = current_user.get_id()
    if user_name != None:
        del_user_file(user_name)
    logout_user()

    return render_template('logout.html')

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
            user['id'] = mongo.db.users.count()
            user['email'] = ''
            user_auth = {}
            user_auth['id'] = mongo.db.user_auths.count()
            user_auth['user_id'] = user['id']
            user_auth['identifier'] = user['name']
            user_auth["identity_type"] = 'name'
            user_auth["credential"] = form.password.data
            mongo.db.users.insert_one(user)
            mongo.db.user_auths.insert_one(user_auth)
            # print(users)

            # 现在不需要复制文件了，登录的时候复制
            # source = "app/static/data/graph_login_test.json"
            # target = "app/static/data/graph_login_test_" + username + ".json"
            # copyfile(source, target)
            # logging.error(mongo.db.users.find({'name':username}))
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    # GET 请求
    return render_template('register.html', form_newuser=form)

@app.route('/slider')
def slider_test():
    return render_template('slider.html')