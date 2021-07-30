#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   image.py
@Time    :   2021/7/1 13:33
@Desc    :   TODO
"""
import json
from time import time, strftime, localtime
from databases import mysqldb as db
from models.historyinfo import HistoryInfo
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from openstackManager.glance import delete_image, get_images_list, set_image_args, create_image, upload_image_data,get_image

from serializers.openstack import (
    openstack_schema
)
from serializers.historyinfo import (
    historyinfo_schema
)
from flask import request
from flask_restful import (
    reqparse,
    Resource
)

from utils.HTTP_Utils import (
    parse_request_url_keys,
    parse_request_data
)
import logging
import sys

sys.path.append('../..')

logger = logging.getLogger('openstack')

# 镜像上传状态信息存储
image_status_info = {'start_time': time(), 'step': 2,
                     'status': 'start', 'message': '准备'}


class ImagesDetail(Resource):
    def get(self, id_md5):
        """
        根据id_md5获取该连接的镜像详细信息
        :param id_md5:
        :return:
        """
        try:  # TODO 逻辑有问题，后续需要修改
            openstack = openstack_schema.get_by_id_md5(id_md5)
            image_lists = get_images_list(auth_ip=openstack.auth_ip, username=openstack.user_name,
                                          password=openstack.password)
            if isinstance(image_lists, tuple):
                logger.error(image_lists[0])
                return {'message': image_lists[0]}, image_lists[1]
            else:
                return {'data': image_lists, 'message': '查询成功'}, 200
        except Exception as e:
            logger.error('获取镜像信息失败: ' + str(e))
            return {'message': '获取镜像信息失败: ' + str(e)}, 400


class ImageUpdate(Resource):
    def patch(self, id):
        parser = reqparse.RequestParser()
        post_keys = parse_request_data(request)
        for _ in post_keys:
            parser.add_argument(_)
        iargs = parser.parse_args()
        boolConvert = {'True': True, 'False': False}
        for key, value in iargs.items():
            iargs[key] = boolConvert.get(value, value)
        try:
            openstack = openstack_schema.get_by_id_md5(iargs['id_md5'])
            iargs.pop('id_md5')
            result = set_image_args(auth_ip=openstack.auth_ip, image_id=id, username=openstack.user_name,
                                    password=openstack.password, **iargs)
            if isinstance(result, tuple):
                logger.error(result[0])
                return {'message': result[0]}, result[1]
            else:
                return {'data': result, 'message': '修改成功'}, 200
        except Exception as e:
            logger.error('修改镜像参数失败: ' + str(e))
            return {'message': '修改镜像参数失败: ' + str(e)}, 400


class ImageCreate(Resource):
    def post(self):
        pass


class ImageDelete(Resource):
    def delete(self):
        pass


class ImageUpload(Resource):
    def __init__(self):
        self.auth_ip = None

    def update_message(self, monitor):
        # 观察者模式，实时获取镜像数据上传时 image_status_info的变化
        global image_status_info
        if monitor.bytes_read % 1000 == 0:
            percent = monitor.bytes_read / monitor.len * 100
            image_status_info = {'start_time': time(), 'step': 2, 'status': 'upload',
                                 'message': self.auth_ip + '上传进度：{:.2f}%'.format(percent)}

    def put(self, name):
        # {'index': '1', 'image_path': '', 'platform': 'linux', 'argList': 'hw_disk_bus=scsi',
        #  'openstack_id_md5_list': '2574edd75751fdccb3668e268a1037c2',
        # 'upload_md5': 'b874c39491a2377b8490f5f1e89761a4'}
        global image_status_info
        # parser = reqparse.RequestParser()
        post_keys = parse_request_data(request)
        # token = request.headers['Authorization']
        # for _ in post_keys:
        #     parser.add_argument(_)
        # TODO 参数暂时不校验
        iargs = post_keys
        history_info = iargs['history_info']
        # iargs['image_path'] = '/vmdata/image-upload/ubuntu18.04-x64-test.raw'
        iargs['upload_md5'] = iargs['upload_md5'][:8] + '-' + iargs['upload_md5'][8:12] + '-' + \
                              iargs['upload_md5'][12:16] + '-' + iargs['upload_md5'][16:20] + '-' + iargs['upload_md5'][
                                                                                                    20:]
        image_status_info = {'start_time': time(), 'step': 2,
                             'status': 'prepare', 'message': '准备上传'}
        # 1 遍历待上传镜像队列
        if isinstance(iargs['openstack_id_md5_list'], str):
            iargs['openstack_id_md5_list'] = [iargs['openstack_id_md5_list']]
        history_info['openstacks_ip'] = []
        history_info['openstacks_name'] = []
        for id_md5 in iargs['openstack_id_md5_list']:
            start_time = time()
            openstack = openstack_schema.get_by_id_md5(id_md5)
            self.auth_ip = openstack.auth_ip
            history_info['openstacks_ip'].append(self.auth_ip)
            history_info['openstacks_name'].append(openstack.platename or 'None')
            image_status_info = {'start_time': start_time, 'step': 2,
                                 'status': 'uploading', 'message': openstack.auth_ip + '准备上传'}
            image_lists = get_images_list(auth_ip=openstack.auth_ip, username=openstack.user_name,
                                          password=openstack.password)
            if isinstance(image_lists, tuple):
                logger.error(openstack.auth_ip + image_lists[0])
                image_status_info = {'start_time': start_time, 'step': 2,
                                     'status': 'error', 'message': openstack.auth_ip + '服务器错误'}
                history_info['action'] += ';' + openstack.auth_ip + '服务器错误'
                continue
            dump_image = {}
            # 检查重名镜像
            for image in image_lists['images']:
                if image['name'] == iargs['image_name']:
                    dump_image = image
                    break
            if dump_image:
                # 2 如果存在同名image
                temp_name = iargs['image_name'] + iargs['upload_md5']
            else:
                temp_name = iargs['image_name']
            image_status_info = {'start_time': start_time, 'step': 2,
                                 'status': 'create', 'message': openstack.auth_ip + '正在创建镜像 ' + temp_name}
            args_list = {arg.split('=')[0]: arg.split('=')[-1] for arg in iargs['argList']}
            args_list['container_format'] = 'bare'
            args_list['disk_format'] = 'raw'
            args_list['visibility'] = 'shared'
            if iargs['platform'] == 'windows':
                args_list['os_type'] = 'windows'
            new_image = create_image(auth_ip=openstack.auth_ip, image_name=temp_name, username=openstack.user_name,
                                     password=openstack.password, **args_list)
            if isinstance(new_image, tuple):
                logger.error(openstack.auth_ip + new_image[0])
                image_status_info = {'start_time': start_time, 'step': 2,
                                     'status': 'error', 'message': openstack.auth_ip + '创建镜像失败 '}
                history_info['action'] += ';' + openstack.auth_ip + ' 创建镜像失败'
                continue
            image_status_info = {'start_time': start_time, 'step': 2,
                                 'status': 'upload', 'message': openstack.auth_ip + '正在上传镜像数据 '}
            # upload = upload_image_data(auth_ip=openstack.auth_ip, image_id=new_image['id'], data_dir=iargs['image_path'], username=openstack.user_name,
            #                             password=openstack.password)
            e = MultipartEncoder(
                fields={
                    'field': (iargs['image_path'], open(iargs['image_path'], 'rb'), 'application/octet-stream')}
            )
            data_stream = MultipartEncoderMonitor(e, self.update_message)
            upload = upload_image_data(auth_ip=openstack.auth_ip, image_id=new_image['id'],
                                       data=data_stream, username=openstack.user_name,
                                       password=openstack.password, by_data=True)
            if isinstance(upload, tuple):
                logger.error(upload[0])
                delete_image(auth_ip=openstack.auth_ip, image_id=new_image['id'], username=openstack.user_name,
                             password=openstack.password)
                image_status_info = {'start_time': start_time, 'step': 2,
                                     'status': 'error', 'message': openstack.auth_ip + '上传镜像数据失败 '}
                history_info['action'] += ';' + openstack.auth_ip + '上传镜像数据失败 '
                continue
            if temp_name != iargs['image_name']:
                # 需要改名
                set_image_args(auth_ip=openstack.auth_ip, image_id=dump_image['id'], username=openstack.user_name,
                               password=openstack.password,
                               **{'name': iargs['image_name'] + '.' + strftime("%Y_%m_%d_%H_%M_%S", localtime())})
                set_image_args(auth_ip=openstack.auth_ip, image_id=new_image['id'], username=openstack.user_name,
                               password=openstack.password, **{'name': iargs['image_name']})
            image_status_info = {'start_time': start_time, 'step': 2,
                                 'status': 'finish' + openstack.auth_ip, 'message': openstack.auth_ip + '完成上传'}
            history_info['action'] += ';' + openstack.auth_ip + '完成上传'
            image = get_image(auth_ip=openstack.auth_ip,uuid=new_image['id'], image_name=temp_name, username=openstack.user_name,
                                     password=openstack.password)
            if not isinstance(image,tuple):
                history_info['checksum'] = image['checksum']
        image_status_info = {'start_time': time(), 'step': 2,
                             'status': 'finish', 'message': '完成上传'}
        history_info['status'] = '成功'
        history_info['openstacks_ip'] = ';'.join(history_info['openstacks_ip'])
        history_info['openstacks_name'] = ';'.join(history_info['openstacks_name'])
        db.session.add(HistoryInfo(**history_info))
        db.session.commit()
        return {'message': '上传完成'}, 200


class ImageUploadInfo(Resource):
    def get(self):
        return {'data': image_status_info}, 200
