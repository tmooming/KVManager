#!/usr/bin/env python
# -*- encoding= utf-8 -*-
"""
@Author  =   TURW
@Contact =   tmooming@163.com
@Software=   PyCharm
@File    =   settings.py
@Time    =   2021/6/4 11=31
@Desc    =   TODO
"""
import os
import sys
import pymysql
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# influxdb
# 2.0 or 1.8
# INFLUXDB_URI = os.environ.get('INFLUXDB_URI', 'http://ts-bp152kjb99d41g2fg.influxdata.rds.aliyuncs.com:3242')
# INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN', 'ella:Test1234')
# 1.7
INFLUXDB_HOST = os.environ.get('INFLUXDB_HOST', '')
INFLUXDB_PORT = os.environ.get('INFLUXDB_PORT', '')
INFLUXDB_SSL = os.environ.get('INFLUXDB_SSL', 'True') # https - True, http - False
INFLUXDB_SSL = True if INFLUXDB_SSL == 'True' else False
INFLUXDB_USERNAME = os.environ.get('INFLUXDB_USERNAME', '')
INFLUXDB_PASSWORD = os.environ.get('INFLUXDB_PASSWORD', '')
INFLUXDB_DB = os.environ.get('INFLUXDB_DB', '')
INFLUXDB_MEASUREMENT = os.environ.get('INFLUXDB_MEASUREMENT', '')

# mysql
MYSQL_CONFIG = {
    'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
    'PORT': os.environ.get('MYSQL_PORT', '3306'),
    'USER': os.environ.get('MYSQL_USER', 'root'),
    'PASSWORD': os.environ.get('MYSQL_PASSWORD', '123456'),
    'DEFAULT_SCHEMA': os.environ.get('MYSQL_DB', 'kvmanager'),
}
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_CONFIG.get('USER')}:{MYSQL_CONFIG.get('PASSWORD')}@{MYSQL_CONFIG.get('HOST')}:{MYSQL_CONFIG.get('PORT')}/{MYSQL_CONFIG.get('DEFAULT_SCHEMA')}"
# for debug info
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# mongodb
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://')

# redis
REDIS_URL = "redis://:123456@localhost:6379/0"

