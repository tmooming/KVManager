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
import datetime

from flask.config import Config
from databases import mysqldb,redis_client
from flask import Flask
from flask_cors import CORS
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

# ============= factory ================
def create_app(configName='production'):
    app = Flask('server')
    Config = config[configName]
    app.config.from_object('settings')
    app.config.from_object(Config)
    CORS(app,supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
    api = Api(app)
    api.init_app(app)
    # init influxdb client
    # influxdb.init_app(app)
    # init mongodb
    # mongodb.init_app(app)
    # init mysqldb
    mysqldb.init_app(app)
    redis_client.init_app(app)
    # init Marshmallow
    ma.init_app(app)
    # register resources
    initialize_routes(api)
    return app


if __name__ == "__main__":
    print('启动-----------------------')
    app = create_app(configName='development')
    app.run(processes=True,host='0.0.0.0',port=5000)