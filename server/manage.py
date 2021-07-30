#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   manage.py
@Time    :   2021/6/4 11:13
@Desc    :   TODO
"""
from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.exceptions import HTTPException

import app as my_app
from error.APIException import APIException
from error.errorcode import ServerError, api_abort

app = my_app.create_app()
manager = Manager(app)
Migrate(app, my_app.mysqldb)
manager.add_command('db', MigrateCommand)

@app.errorhandler(Exception)
def framework_error(e):
    print('出发------------------')
    # 判断异常是不是APIException
    if isinstance(e, APIException):
        return e
    # 判断异常是不是HTTPException
    if isinstance(e, HTTPException):
        code = e.code
        # 获取具体的响应错误信息
        msg = e.description
        error_code = 1007
        return APIException(code=code, msg=msg, error_code=error_code)
    # 异常肯定是Exception
    else:
        # 如果是调试模式,则返回e的具体异常信息。否则返回json格式的ServerException对象！
        # 针对于异常信息，我们最好用日志的方式记录下来。
        if app.config["DEBUG"]:
            return e
        else:
            return ServerError()

class ValidationError(ValueError):
    pass

@app.errorhandler(ValidationError)
def validation_error(e):
    return api_abort(400, e.args[0])

#
# @app.after_request
# def af_req(resp):  #解决跨域session丢失
#     response = make_response(resp)
#     print(resp)
#     response.headers['Access-Control-Allow-Origin'] = resp.environ['HTTP_ORIGIN']
#     response.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,DELETE,OPTIONS'
#     #resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild'
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#
#     # response.headers['X-Powered-By'] = '3.2.1'
#     response.headers['Content-Type'] = 'application/json;charset=utf-8'
#     return response

if __name__ == '__main__':
    print('sa',app.url_map)
    manager.run()