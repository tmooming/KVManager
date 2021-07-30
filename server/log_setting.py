#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   log_setting.py
@Time    :   2021/6/4 13:32
@Desc    :   TODO
"""
import formatter
import os
import time

# setting_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import re
from logging.handlers import TimedRotatingFileHandler

setting_path = os.path.dirname(os.path.abspath(__file__))
BASE_DIR_LOG = os.path.join(os.path.sep, setting_path, 'logs')
# 设置生成日志文件名的格式，以年-月-日来命名
# suffix设置，会生成文件名为log.2020-02-25.log
time_now = time.strftime("%Y-%m-%d", time.localtime())
SUFFIX = time_now+'.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'app': {
            "class":"logging.handlers.TimedRotatingFileHandler",
            # 'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(os.path.sep, BASE_DIR_LOG,'app', 'app-'+SUFFIX),
            # 'mode': 'a',
            'encoding': 'utf8',
            # 'maxBytes': 1024 * 1024 * 5,
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        },
        'user': {
            "class":"logging.handlers.TimedRotatingFileHandler",
            # 'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(os.path.sep, BASE_DIR_LOG,'user', 'user-'+SUFFIX),
            # 'mode': 'a',
            'encoding': 'utf8',
            # 'maxBytes': 1024 * 1024 * 5,
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        },
        'compute': {
            "class":"logging.handlers.TimedRotatingFileHandler",
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(os.path.sep, BASE_DIR_LOG,'compute', 'compute-'+SUFFIX),
            'encoding': 'utf8',
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        },
        'instance': {
            "class":"logging.handlers.TimedRotatingFileHandler",
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(os.path.sep, BASE_DIR_LOG,'instance', 'instance-'+SUFFIX),
            'encoding': 'utf8',
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        },
        'openstack': {
            "class":"logging.handlers.TimedRotatingFileHandler",
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(os.path.sep, BASE_DIR_LOG,'openstack', 'openstack-'+SUFFIX),
            'encoding': 'utf8',
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        },
    },
    'formatters': {
        'verbose': {
            # 'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            # 'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(process)d %(thread)d %(message)s'
            'format': "[%(asctime)s] - %(filename)s [line:%(lineno)d] %(name)s - %(levelname)s: %(message)s"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'loggers': {
        'wsgi': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'app': {
            'handlers': ['console', 'app'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'user': {
            'handlers': ['console', 'user'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'compute': {
            'handlers': ['console', 'compute'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'instance': {
            'handlers': ['console', 'instance'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'openstack': {
            'handlers': ['console', 'openstack'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}