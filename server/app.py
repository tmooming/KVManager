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
import sys
import time
from pprint import pformat

from flask.config import Config
from databases import mysqldb, redis_client
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from logging.config import dictConfig

from routes import initialize_routes
from serializers import ma
import logging
import os
import settings
from config import config, LOG_FORMAT
from loguru import logger


# configuration
#
# try:
#     from log_setting import LOGGING
#
#     dictConfig(LOGGING)
# except Exception as e:
#     pass


# logger = logging.getLogger('app')

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict) -> str:
    format_string = LOG_FORMAT

    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


# ============= factory ================
def create_app(configName='production'):
    app = Flask('server')
    Config = config[configName]
    app.config.from_object('settings')
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
    api = Api(app)
    api.init_app(app)
    # init influxdb client
    # influxdb.init_app(app)
    # init mongodb
    # mongodb.init_app(app)
    # init mysqldb
    app_log = os.path.join(os.getcwd(), f'logs/app/app_{time.strftime("%Y_%m_%d")}.log')
    compute_log = os.path.join(os.getcwd(), f'logs/compute/compute_{time.strftime("%Y_%m_%d")}.log')
    instance_log = os.path.join(os.getcwd(), f'logs/instance/instance_{time.strftime("%Y_%m_%d")}.log')
    openstack_log = os.path.join(os.getcwd(), f'logs/openstack/openstack_{time.strftime("%Y_%m_%d")}.log')
    # log_name = '/home/imagemgr/KVManager/server/logs/app/app.log'
    logging.basicConfig(handlers=[InterceptHandler(level='INFO')], level='INFO')
    logger.configure(handlers=[{"sink": sys.stderr, "level": 'INFO'}])  # 配置日志到标准输出流
    logger.add(app_log, rotation="00:00",
               filter=lambda record: record['extra'].get('name') not in ['compute', 'instance', 'openstack'],
               retention='30 days', enqueue=True, encoding='utf-8', colorize=False,
               level='WARNING', compression='zip')  # 配置日志到输出到文件
    logger.add(compute_log, filter=lambda record: record['extra'].get("name") == "compute", rotation="00:00",
               retention='30 days', enqueue=True, encoding='utf-8', colorize=False, level='INFO', compression='zip')
    logger.add(instance_log, filter=lambda record: record['extra'].get("name") == "instance", rotation="00:00",
               retention='30 days', enqueue=True, encoding='utf-8', colorize=False, level='INFO', compression='zip')
    logger.add(openstack_log, filter=lambda record: record['extra'].get("name") == "openstack", rotation="00:00",
               retention='30 days', enqueue=True, encoding='utf-8', colorize=False, level='INFO', compression='zip')
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
    app.run(processes=True, host='0.0.0.0', port=5000)
