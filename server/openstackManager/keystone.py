#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   keystone.py
@Time    :   2021/6/30 9:59
@Desc    :   获取、验证token，目前仅限于Password authentication with scoped by domain authorization
"""

import json
import sys

sys.path.append('..')
import requests
from utils.Openstack_Utils import (
    set_token_request_json,
    set_headers,
    get_error_message
)

OS_AUTH_URL = 'http://10.122.103.8'

"""
上传步骤
1. 选择平台（多选）
2. 虚拟机关机
3. 拷贝文件
"""


def get_token_by_requests(auth_ip: str, keystone_port=5000, username=None, userid=None, password=None, domain_name=None,
                          domain_id=None):
    request_body = set_token_request_json(username=username, password=password)
    if isinstance(request_body, str):
        return '参数错误', request_body
    get_token_url = 'http://' + auth_ip + ':' + str(keystone_port) + '/v3/auth/tokens'
    request_headers = set_headers()
    response = requests.post(get_token_url, headers=request_headers, data=json.dumps(request_body))
    if response.status_code < 400:
        token = response.headers['X-Subject-Token']
        return token
    else:
        return get_error_message(response.status_code)


def validate_token(auth_ip: str, keystone_port=5000, username=None, userid=None, password=None, domain_name=None,
                          domain_id=None):
    token = get_token_by_requests(auth_ip='10.122.103.8', username='turw1', password='abcd-1234')
    if isinstance(token, tuple):
        return token
    # X-Subject-Token:待验证身份令牌，X-Auth-Token:本人身份令牌
    headers = {'X-Subject-Token': token, 'X-Auth-Token': token}
    request_headers = set_headers(**headers)
    validate_token_url = 'http://' + auth_ip + ':' + str(keystone_port) + '/v3/auth/tokens'
    response = requests.get(validate_token_url, headers=request_headers)
    if response.status_code == 200:
        return 200, 'token有效'
    else:
        return get_error_message(response.status_code)



if __name__ == '__main__':
    host = '192.168.159.134'
    login = 'admin'
    passwd = 'admin'
    conn = 1
    get_token_by_requests(auth_ip='10.122.103.8',username='turw1',password='abcd-1234')
