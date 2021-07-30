#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   HTTP_Utils.py
@Time    :   2021/6/4 13:26
@Desc    :   HTTP解析
"""
import ast
import hashlib
import json
import os
from datetime import datetime, timezone
# import pytz
import time
import uuid


def MD5_Strs(str):
    md = hashlib.md5()  # 创建md5对象
    md.update(str.encode(encoding='utf-8'))
    return md.hexdigest()

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

copy_percent = 0
def GetFileMd5AandCopy(inputname,outputname):
    if not os.path.isfile(inputname):
        return
    global copy_percent
    inhash = hashlib.md5()
    outhash = hashlib.md5()
    size = os.path.getsize(inputname)/8096
    input = open(inputname,'rb')
    out = open(outputname,'wb')
    count = 0
    while True:
        block = input.read(8096)
        count+=1
        copy_percent = round(count/size,2)
        if not block :
            break
        out.write(block)
        inhash.update(block)
        outhash.update(block)
    input.close()
    out.close()
    return inhash.hexdigest(), outhash.hexdigest()

def getCopyPercent():
    return copy_percent

def parse_request_args_keys(request):
    '''
    In a GET request, return all query params keys
    '''
    query_args = request.args
    return [_ for _ in query_args]

def parse_request_url_keys(request):
    '''
    In a POST request, return all post params keys from vue axios
    '''
    data = dict(request.args)
    return data

def parse_request_data(request):
    '''
    :param request:
    :return:
    '''
    # data = ast.literal_eval(str(request.data, encoding='utf8'))
    data = json.loads(request.data)
    return data


def parse_request_json_keys(request):
    '''
    In a POST request, return all post params keys
    '''
    post_data = request.json
    return [_ for _ in post_data]


def generate_user_id():
    '''
    Generate a UUID for user_id
    '''
    user_id = uuid.uuid4().hex
    return user_id


def convert_string_2_timestamp(datetime_string):
    try:
        res = int(time.mktime(datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ").timetuple()))
        # res = int(time.mktime(datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ").timetuple()) * 1000000000)
    except:
        res = int(time.mktime(datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S").timetuple()))
    return res


def convert_timestamp_2_UTC8_datetimestring(timestamp):
    # local_tz = pytz.timezone('Asia/Shanghai')
    # dt = datetime.fromtimestamp(timestamp, tz=local_tz)

    # convert timestamp to UTC+8 timestamp
    utc8_timestamp = timestamp + 8 * 60 * 60
    dt = datetime.fromtimestamp(utc8_timestamp)
    dt_string = dt.strftime("%Y-%m-%dT%H:%M:%S")
    return dt_string


def convert_UTCstring_2_UTC8string(datetime_string):
    ts = convert_string_2_timestamp(datetime_string)
    dt_str = convert_timestamp_2_UTC8_datetimestring(ts)
    return dt_str