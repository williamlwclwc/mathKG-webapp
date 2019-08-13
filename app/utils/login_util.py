users = [
    {'username': 'Tom', 'password': '111111'},
    {'username': 'Michael', 'password': '123456'},
    {'username': 'xlitong', 'password':'111111'}
]

# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(username):
    for user in users:
        if user['username'] == username:
            return user