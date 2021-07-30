"""
    *************************** 
    --------description-------- 
 	 Description: 
 	 Version: 1.0
 	 Autor: Tu Ruwei
 	 Date: 2021-07-13 17:18:43
 	 LastEditors: Tu Ruwei
 	 LastEditTime: 2021-07-14 16:00:57

    ***************************  
"""
from flask.config import Config
from databases import mysqldb
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask import session
from flask_restful import Api
from logging.config import dictConfig

from routes import initialize_routes
from serializers import ma
import logging
import os
import settings
from config import config
# configuration

try:
    from log_setting import LOGGING
    dictConfig(LOGGING)
except Exception as e:
    pass

logger = logging.getLogger('app')

errors = {
    # StandardError(Exception)的子类
    "TypeError":{
        'message': "TypeError 错误信息已被修改",
        'status': 200,
        'extra': "TypeError 被修改了，你看吧",
    },
    # HTTPException的子类
    "BadRequest":{
        'message': "BadRequest 错误信息已被修改",
        'status': 200,
        'extra': "BadRequest 被修改了，你看吧",
    }
}

# ============= factory ================
def create_app(configName='production'):
    app = Flask('server')
    Config = config[configName]
    app.config.from_object('settings')
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'qwertyuioplkjhgfdsazxcvb'
    CORS(app,supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
    api = Api(app)
    api.init_app(app)
    # register_errors(app)
    #sessions.init_app(app)
    # init influxdb client
    # influxdb.init_app(app)
    # init mongodb
    # mongodb.init_app(app)
    # init mysqldb
    mysqldb.init_app(app)
    # init Marshmallow
    ma.init_app(app)
    # register resources
    initialize_routes(api)
    return app


if __name__ == "__main__":
    print('启动-----------------------')
    app = create_app(configName='development')
    app.run(processes=True,host='0.0.0.0',port=5000)