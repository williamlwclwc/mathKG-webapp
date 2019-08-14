from flask import Flask
from flask_login import LoginManager 
from flask_pymongo import PyMongo
# from app import views

app = Flask(__name__)
# app.config.from_object('config')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# 配置mongodb
app.config['MONGO_URI'] = r'mongodb://127.0.0.1:27017/MiddleSchoolMathDB'
app.config['MONGO_DBNAME'] = 'MiddleSchoolMathDB'
mongo = PyMongo(app)

#login
login_manager = LoginManager(app)
# 设置登录视图的名称，如果一个未登录用户请求一个只有登录用户才能访问的视图
# 则闪现一条错误消息，并重定向到这里设置的登录视图
# 如果未设置登录视图，则直接返回401错误
login_manager.login_view = 'login'
# 设置当未登录用户请求一个只有登录用户才能访问的视图时，闪现的错误消息的内容，
# 默认的错误消息是：Please log in to access this page.。
login_manager.login_message = 'Unauthorized User'
# 设置闪现的错误消息的类别
login_manager.login_message_category = "info"

from app import views