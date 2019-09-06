import glob
import os
import logging

# 登出时删除所有该用户的用户文件
def del_user_file(user_name):
    user_files = glob.glob("./app/static/data/graph_login_test_" + user_name + "*.json")
    user_files += glob.glob("./app/static/rawdata/" + user_name + "*_change.json")
    user_files += glob.glob("./app/static/rawdata/" + user_name + "*_merged.json")
    logging.error(user_files)
    for user_file in user_files:
        os.remove(user_file)
