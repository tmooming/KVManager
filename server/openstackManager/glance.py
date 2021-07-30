#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   glance.py
@Time    :   2021/6/30 14:09
@Desc    :   image管理
'''
import base64
import datetime
import json
import platform
import sys

import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

if platform.system() == 'Windows':
    from keystone import get_token_by_requests
elif platform.system() == 'Linux':
    from .keystone import get_token_by_requests

sys.path.append('..')
from utils.Openstack_Utils import get_error_message, set_headers, set_image_arg


def get_image(auth_ip: str,uuid, glance_port='9292', keystone_port=5000, username=None, userid=None, password=None,
                    domain_name=None, domain_id=None, token=None, **kwargs):
    prev_url = 'http://' + auth_ip + ':' + str(glance_port)
    images_list_url = '/v2/images/'+uuid
    if not token:
        token = get_token_by_requests(auth_ip=auth_ip, username=username, password=password)
    if isinstance(token, tuple):
        return token
    headers = set_headers(**{'X-Auth-Token': token})
    response = requests.get(prev_url + images_list_url, headers=headers)
    if response.status_code < 400:
        return response.json()
    else:
        return get_error_message(response.status_code)

def get_images_list(auth_ip: str, glance_port='9292', keystone_port=5000, username=None, userid=None, password=None,
                    domain_name=None, domain_id=None, token=None, **kwargs):
    prev_url = 'http://' + auth_ip + ':' + str(glance_port)
    images_list_url = '/v2/images?sort=name:asc,status:desc'
    if not token:
        token = get_token_by_requests(auth_ip=auth_ip, username=username, password=password)
    if isinstance(token, tuple):
        return token
    headers = set_headers(**{'X-Auth-Token': token})
    result = {'images': []}
    for flag in ['true', 'false']:
        kwargs.update({'os_hidden': flag})
        response = requests.get(prev_url + images_list_url, headers=headers, params=kwargs)
        if response.status_code < 400:
            response = response.json()
            result['images'].extend(response['images'])
            while response.get('next', None):
                response = requests.get(prev_url + response['next'], headers=headers, params=kwargs)
                if response.status_code < 400:
                    response = response.json()
                    result['images'].extend(response['images'])
                else:
                    return get_error_message(response.status_code)
        else:
            return get_error_message(response.status_code)
    kwargs.pop('os_hidden')
    return result

def set_image_args(auth_ip: str, image_id: str, glance_port='9292', keystone_port=5000, username=None, userid=None,
                   password=None, domain_name=None, domain_id=None, token=None, **kwargs):
    prev_url = 'http://' + auth_ip + ':' + str(glance_port)
    set_image_url = '/v2/images/' + image_id
    if not token:
        token = get_token_by_requests(auth_ip=auth_ip, username=username, password=password)
    if isinstance(token, tuple):
        return token
    headers = set_headers(**{'X-Auth-Token': token, 'Content-Type': 'application/openstack-images-v2.1-json-patch'})
    args = set_image_arg(**kwargs)
    response = requests.patch(url=prev_url + set_image_url, headers=headers, data=args)
    if response.status_code < 400:
        return {'images': [json.loads(response.text)]}
    else:
        return response.reason, response.status_code


def create_image(auth_ip: str, image_name, glance_port='9292', keystone_port=5000, username=None, userid=None,
                 password=None, domain_name=None, domain_id=None, token=None, **kwargs):
    prev_url = 'http://' + auth_ip + ':' + str(glance_port)
    create_image_url = '/v2/images'
    body = {key: value for key, value in kwargs.items()}
    body['name'] = image_name
    if not token:
        token = get_token_by_requests(auth_ip=auth_ip, username=username, password=password)
    if isinstance(token, tuple):
        return token
    headers = set_headers(**{'X-Auth-Token': token})
    response = requests.post(url=prev_url + create_image_url, headers=headers, data=json.dumps(body))
    if response.status_code < 400:
        return response.json()
    else:
        return response.reason, response.status_code

def upload_image_data(auth_ip: str, image_id: str, data, store_identifier=None, glance_port='9292',
                      keystone_port=5000, username=None, userid=None, password=None, domain_name=None, domain_id=None,
                      token=None,by_data=False):
    prev_url = 'http://' + auth_ip + ':' + str(glance_port)
    create_image_url = '/v2/images/' + image_id + '/file'
    if not token:
        token = get_token_by_requests(auth_ip=auth_ip, username=username, password=password)
    if isinstance(token, tuple):
        return token
    headers = set_headers(
        **{'X-Auth-Token': token, 'Content-Type': 'application/octet-stream', 'X-Image-Meta-Store': store_identifier})
    # e = MultipartEncoder(
    #     fields={
    #         'field1': (data, open(data, 'rb'), 'application/octet-stream')}
    # )
    # m = MultipartEncoderMonitor(e, my_callback)
    if by_data:
        response = requests.put(url=prev_url + create_image_url, headers=headers, data=data)
    else:
        # response = requests.put(url=prev_url + create_image_url, headers=headers, data=data)
        response = requests.put(url=prev_url + create_image_url, headers=headers, data=open(data, 'rb'))
    if response.status_code < 400:
        return response.text
    else:
        return response.reason, response.status_code


def delete_image(auth_ip: str, image_id: str, glance_port='9292', keystone_port=5000, username=None, userid=None,
                 password=None, domain_name=None, domain_id=None, token=None):
    prev_url = 'http://' + auth_ip + ':' + str(glance_port)
    delete_image_url = '/v2/images/' + image_id
    if not token:
        token = get_token_by_requests(auth_ip=auth_ip, username=username, password=password)
    if isinstance(token, tuple):
        return token
    headers = set_headers(**{'X-Auth-Token': token})
    response = requests.delete(url=prev_url + delete_image_url, headers=headers)
    if response.status_code < 400:
        return '删除成功'
    else:
        return response.reason, response.status_code


if __name__ == '__main__':
    set_args = [{
        'op': 'replace',
        'path': '/os_hidden',
        'value': True
    }]
    dicts = {'hw_disk_bus': 'scsi', 'hw_firmware_type': 'uefi', 'hw_scsi_model': 'virtio-scsi'}
    # upload_image_data(auth_ip='10.122.103.8',image_id='b2173dd3-7ad6-4362-baa6-a68bce356511',data_dir='/data/镜像/ubuntu_mini.qcow2', username='turw1', password='abcd-1234')
    # res = create_image(auth_ip='10.122.103.8',image_name='test', username='turw1', password='abcd-1234',**dicts)
    res = delete_image(auth_ip='10.122.103.8', image_id='0c510516-583a-4cf7-8f74-40cbdf30bb66', username='turw1',
                password='abcd-1234')
    # res = get_images_list(auth_ip='10.122.103.8', username='turw1', password='abcd-1234')
    # res = set_image_args(auth_ip='10.122.103.8', image_id='a29ee84f-879d-4bd3-9d9f-7d2a3b131de6', username='turw1',
    #                password='abcd-1234', **{'hw_disk_bus':'scsi'})
    print(res)
    # with open('/data/镜像/ubuntu_mini.qcow2', 'rb') as f:
    #     # 读取二进制序列
    #     data = f.read()
    #     # b64编码，生成新的可字符化的二进制序列
    #     bast64_data = base64.b64encode(data)
    #     # 字符串化，使用utf-8的方式解析二进制
    #     bast64_str = str(bast64_data, 'utf-8')
    #     print(json.loads(bast64_str))
