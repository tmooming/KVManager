#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   Openstack_Utils.py
@Time    :   2021/6/30 11:23
@Desc    :   对openstack请求的封装
"""

import json


def set_token_request_json(username=None, userid=None, password=None, domainname=None, domainid=None):
    """
    Domain-Scoped with Domain Name
    :param username:
    :param userid:
    :param password:
    :param domainname:
    :param domainid:
    :return:
    """
    body = {'auth':
                {'identity':
                     {'methods': ['password'],
                      'password': {
                          'user': {
                              'domain': {
                                  'name': 'default'
                              },
                              'name': 'turw1',
                              'password': 'abcd-1234'
                          }
                      }
                      },
                 'scope': {
                     'project': {
                         'domain': {
                         },
                         'name': 'admin'
                     }
                 }
                 }
            }
    if username:
        body['auth']['identity']['password']['user']['name'] = username
    elif userid:
        body['auth']['identity']['password']['user']['id'] = userid
    else:
        return "用户名或用户ID不能为空"
    if password:
        body['auth']['identity']['password']['user']['password'] = password
    else:
        return "密码不能为空"
    if domainname:
        body['auth']['scope']['project']['domain']['name'] = domainname
    elif domainid:
        body['auth']['scope']['project']['domain']['id'] = domainid
    else:
        body['auth']['scope']['project']['domain']['name'] = 'default'
    return body


def set_headers(**kwargs):
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = '*/*'
    for key, value in kwargs.items():
        headers[key] = value
    return headers


def get_error_message(status_code):
    if status_code == 400:
        return '参数错误，请校验', 400
    elif status_code == 401:
        return '用户必须在发出请求之前进行身份验证。', 401
    elif status_code == 403:
        return '策略不允许当前用户执行此操作。', 403
    elif status_code == 404:
        return '找不到请求的资源', 404


def set_image_arg(**kwargs):
    args = []
    for key, value in kwargs.items():
        item = {
            'op': 'replace',
            'path': '/' + key,
            'value': value
        }
        args.append(item)
    return json.dumps(args)


if __name__ == '__main__':
    set_image_args()
