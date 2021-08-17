#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   connection.py
@Time    :   2021/6/30 14:41
@Desc    :   连接openstack服务器
"""
import ast
import json

from databases import mysqldb as db
from models.openstack import Openstack
from serializers.openstack import (
    openstack_schema
)
from flask import request
from flask_restful import (
    reqparse,
    Resource
)
from flask import session
from utils.SqlToDict import queryToDict
from utils.HTTP_Utils import (
    parse_request_url_keys,
    MD5_Strs,
    parse_request_data
)
import logging
from loguru import logger as logger_openstack
import sys
sys.path.append('../..')
from openstackManager.keystone import get_token_by_requests
#logger = logging.getLogger('openstack')
logger = logger_openstack.bind(name="openstack")

class OpenstackConnect(Resource):
    """
    建立连接，及获取连接信息
    """
    def get(self):
        infos = []
        openstacks = openstack_schema.get_all_openstacks()
        if openstacks:
            for openstack in openstacks:
                token = get_token_by_requests(auth_ip=openstack.auth_ip, username=openstack.user_name, password=openstack.password)
                if token!=openstack.token:
                    try:
                        db.session.query(Openstack).filter(Openstack.id_md5 == openstack.id_md5,
                                                         Openstack.delete_sig == 0).update(
                            {'token': token})
                        db.session.commit()
                        logger.info(openstack.auth_ip+' token更新成功')
                    except Exception as e:
                        logger.error('token更新失败：' + str(e))
            infos = queryToDict(openstacks)
            logger.info('连接信息查询成功')
            return {'data': infos,'message':'查询成功'},200
        else:
            logger.info('暂无连接，请添加连接')
            return {'data':infos,'message':'暂无连接，请添加连接'},201

    def post(self):
        parser = reqparse.RequestParser()
        post_keys = parse_request_data(request)
        # for _ in post_keys:
        #     parser.add_argument(_)
        # iargs = parser.parse_args()
        iargs = post_keys
        # user = ast.literal_eval(iargs['user'])
        # domain = ast.literal_eval(iargs['domain'])
        iargs[iargs['user']['type']] = iargs['user']['value']
        iargs[iargs['domain']['type']] = iargs['domain']['value']
        iargs.pop('user')
        iargs.pop('domain')
        id_md5 = MD5_Strs(''.join(iargs.values()))
        iargs['id_md5'] = id_md5
        error = openstack_schema.validate(iargs)
        if error:
            logger.error('参数错误，请检查')
            return {'message':'参数错误，请检查'},401
        sig = openstack_schema.validate_id_md5(id_md5)
        if sig == 1:  # 如果连接已存在，且delete_sig为0，则返回错误信息
            logger.error("该连接已存在")
            return {'message': '该连接已存在'}, 400
        else:  # 否则，尝试连接
            # if user['type'] == 'user_name' and domain['type'] == 'domain_name':
            token = get_token_by_requests(auth_ip=iargs['auth_ip'], username=iargs['user_name'], password=iargs['password'])
            if isinstance(token,str):
                if sig == 2:  # 如果连接已存在，但delete_sig为1，则修改delete_sig
                    try:
                        db.session.query(Openstack).filter(Openstack.id_md5 == id_md5,
                                                         Openstack.delete_sig == 1).update(
                            {'delete_sig': 0})
                        db.session.commit()
                        db.session.close()
                    except Exception as e:
                        logger.error('更新失败：' + str(e))
                        return {'message': str(e)}, 400
                elif sig == 3:  # 如果数据库内没有该记录，则尝试新增该记录
                    iargs['token'] = token
                    openstack = Openstack(**iargs)
                    try:
                        db.session.add(openstack)
                        db.session.commit()
                    except Exception as e:
                        logger.error('入库失败: ' + str(e))
                        return {'message':'入库失败'},401
                logger.info('连接成功')
                openstack = openstack_schema.get_by_id_md5(id_md5)
                return {'data': queryToDict(openstack), 'message': '连接成功'}, 201
            else:
                logger.error(token[0])
                return {'message':token[0]},token[1]


class OpenstackDisconnect(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        post_keys = parse_request_url_keys(request)
        for _ in post_keys:
            parser.add_argument(_)
        iargs = parser.parse_args()
        openstack = openstack_schema.get_by_id_md5(iargs['id_md5'])
        try:
            db.session.query(Openstack).filter(Openstack.id_md5 == openstack.id_md5, Openstack.delete_sig == 0).update(
                {'delete_sig': 1})
            # db.session.query(Compute).filter(Compute.token == compute.token).delete()
            db.session.commit()
            logger.info('删除成功')
            return {'message': '删除成功'}, 204
        except Exception as e:
            logger.info('删除失败：' + str(e))
            return {'message': '删除失败'}, 400
if __name__ == '__main__':
    pass
