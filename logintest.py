from flask import Flask, render_template, request, redirect, url_for, flash, abort, Blueprint
from flask_login import (LoginManager, UserMixin, login_user, logout_user,
                            current_user, login_required, fresh_login_required)

login_test = Blueprint('login_test', __name__, template_folder='templates')

login_manager = LoginManager(login_test)
# 设置登录视图的名称，如果一个未登录用户请求一个只有登录用户才能访问的视图，
# 则闪现一条错误消息，并重定向到这里设置的登录视图。
# 如果未设置登录视图，则直接返回401错误。
login_manager.login_view = 'login'
# 设置当未登录用户请求一个只有登录用户才能访问的视图时，闪现的错误消息的内容，
# 默认的错误消息是：Please log in to access this page.。
login_manager.login_message = 'Unauthorized User'
# 设置闪现的错误消息的类别
login_manager.login_message_category = "info"

users = [
    {'username': 'Tom', 'password': '111111'},
    {'username': 'Michael', 'password': '123456'}
]

class User(UserMixin):
    pass

# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(username):
    for user in users:
        if user['username'] == username:
            return user

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

@login_test.route('/hello-test')
@login_required
def index():
    return render_template('hello-test.html')

@login_test.route('/home-test')
@fresh_login_required
def home():
    return 'Logged in as: %s' % current_user.get_id()

@login_test.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = query_user(username)
        # 验证表单中提交的用户名和密码
        if user is not None and request.form['password'] == user['password']:
            curr_user = User()
            curr_user.id = username

            # 通过Flask-Login的login_user方法登录用户
            login_user(curr_user, remember=True)

            # 如果请求中有next参数，则重定向到其指定的地址，
            # 没有next参数，则重定向到"index"视图
            next = request.args.get('next')
            return redirect(next or url_for('index'))

        flash('Wrong username or password!')
    # GET 请求
    return render_template('login.html')

@login_test.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'


