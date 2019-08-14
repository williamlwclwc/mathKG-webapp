# users = [
#     {'username': 'Tom', 'password': '111111'},
#     {'username': 'Michael', 'password': '123456'},
#     {'username': 'xlitong', 'password':'111111'}
# ]
from app import mongo
from flask import  flash

# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(username):
    users = mongo.db.users.find({},{'_id':0})
    for user in users:
        if user['name'] == username:
            return user