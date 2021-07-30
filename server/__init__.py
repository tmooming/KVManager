"""
    *************************** 
    --------description-------- 
 	 Description: 
 	 Version: 1.0
 	 Autor: Tu Ruwei
 	 Date: 2021-07-13 17:18:43
 	 LastEditors: Tu Ruwei
 	 LastEditTime: 2021-07-14 16:09:39

    ***************************  
"""
# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# """
# @Author  :   TURW
# @Contact :   tmooming@163.com
# @Software:   PyCharm
# @File    :   __init__.py
# @Time    :   2021/6/3 13:54
# @Desc    :   TODO
# """
# import os
# from flask import Flask
# from flask_cors import CORS
# from tests import test_blue
# from user import user_blue
# import platform
# # configuration
# DEBUG = True
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.join(BASE_DIR, 'server/static'))
# print(platform.system()=="Windows")
# # instantiate the app
# def create_app():
#     # 建立静态文件static，tamplates的路径
#     if platform.system()=="Windows":
#         static_dir = os.path.join(BASE_DIR, r'server\static')
#         templates_dir = os.path.join(BASE_DIR, r'server\templates')
#     else:
#         static_dir = os.path.join(BASE_DIR, r'server/static')
#         templates_dir = os.path.join(BASE_DIR, r'server/templates')
#     app = Flask(__name__,template_folder=templates_dir,static_folder=static_dir)
#     app.config.from_object(__name__)
#     app.register_blueprint(test_blue)
#     app.register_blueprint(user_blue,url_prefix = '/user')
#     # enable CORS
#     return app
#
#
#
#