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
import os
import time
import multiprocessing
from logging.handlers import TimedRotatingFileHandler
from logging import FileHandler

#lock = multiprocessing.Lock()


class SafeLog(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False):
        TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay, utc)

    """
    Override doRollover
    lines commanded by "##" is changed by cc
    """

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.

        Override,   1. if dfn not exist then do rename
                    2. _open with "a" model
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        ##        if os.path.exists(dfn):
        ##            os.remove(dfn)

        # Issue 18940: A file may not have been created if delay is True.
        ##        if os.path.exists(self.baseFilename):
        if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.mode = "a"
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt

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
            #"class": "mrfh.MultiprocessRotatingFileHandler",
            "class":"SafeLog",
            # "class":"logging.handlers.TimedRotatingFileHandler",
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
            # "class": "mrfh.MultiprocessRotatingFileHandler",
            "class": "SafeLog",
            #"class":"logging.handlers.TimedRotatingFileHandler",
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
             #"class": "mrfh.MultiprocessRotatingFileHandler",
            "class":"SafeLog",
            # "class":"logging.handlers.TimedRotatingFileHandler",
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(os.path.sep, BASE_DIR_LOG,'compute', 'compute-'+SUFFIX),
            'encoding': 'utf8',
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        },
        'instance': {
             #"class": "mrfh.MultiprocessRotatingFileHandler",
            "class":"SafeLog",
            #"class":"logging.handlers.TimedRotatingFileHandler",
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(os.path.sep, BASE_DIR_LOG,'instance', 'instance-'+SUFFIX),
            'encoding': 'utf8',
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        },
        'openstack': {
             #"class": "mrfh.MultiprocessRotatingFileHandler",
            "class":"SafeLog",
            #"class":"logging.handlers.TimedRotatingFileHandler",
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(os.path.sep, BASE_DIR_LOG,'openstack', 'openstack-'+SUFFIX),
            'encoding': 'utf8',
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        },
        # 'gunicorn_access': {
        #     "class": "mrfh.MultiprocessRotatingFileHandler",
        #     #"class":"MultiProcessSafeDailyRotatingFileHandler",
        #     #"class":"logging.handlers.TimedRotatingFileHandler",
        #     'level': 'DEBUG',
        #     'formatter': 'verbose',
        #     'filename': os.path.join(os.path.sep, BASE_DIR_LOG,'gunicorn_access', 'gunicorn_access-'+SUFFIX),
        #     'encoding': 'utf8',
        #     'when': 'D',
        #     'interval': 1,
        #     'backupCount': 30,
        # },
        # 'gunicorn_error': {
        #     "class": "mrfh.MultiprocessRotatingFileHandler",
        #     #"class":"MultiProcessSafeDailyRotatingFileHandler",
        #     #"class":"logging.handlers.TimedRotatingFileHandler",
        #     'level': 'DEBUG',
        #     'formatter': 'verbose',
        #     'filename': os.path.join(os.path.sep, BASE_DIR_LOG, 'logs/gunicorn_error', 'gunicorn_error-' + SUFFIX),
        #     'encoding': 'utf8',
        #     'when': 'D',
        #     'interval': 1,
        #     'backupCount': 30,
        # }
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
        # 'gunicorn_access': {
        #     'handlers': ['console', 'gunicorn_access'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
        # 'gunicorn_error': {
        #     'handlers': ['console', 'gunicorn_error'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
    },
}