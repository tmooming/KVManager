#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   connection.py
@Time    :   2021/6/10 12:33
@Desc    :   TODO
"""
import datetime

from sqlalchemy import desc

from databases import mysqldb as db
from models.computes import Compute
from models.historyinfo import HistoryInfo
from libvirt import libvirtError, virConnect
from serializers.computes import (
    compute_schema,
    compute_token_schema
)
from serializers.historyinfo import historyinfo_schema
from flask import request
from flask_restful import (
    reqparse,
    Resource
)
from flask import session
from utils.HTTP_Utils import (
    parse_request_url_keys,
    MD5_Strs
)
import logging
import sys

from utils.SqlToDict import queryToDict
from vrtManager.connection import wvmConnect, connection_manager
from vrtManager.hostdetails import wvmHostDetails
from vrtManager.storage import wvmStorages
from vrtManager.network import wvmNetworks
from vrtManager.interface import wvmInterfaces, wvmInterface
from vrtManager.nwfilters import wvmNWFilters

logger = logging.getLogger('compute')


class HostInfo(Resource):
    """
    从数据库获取宿主机信息
    """

    def get(self):
        infos = []
        if compute_schema.get_all_computes():
            computes = compute_schema.get_all_computes()
            for compute in computes:
                # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
                if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                        connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                          compute.type), virConnect):
                    vm = wvmHostDetails(compute.hostip, compute.user, compute.password,
                                        compute.type)
                    info = vm.get_connect_info()
                    info['token'] = compute.token
                    info['message'] = '已连接'
                    try:
                        # 将连接信息入库，该步骤允许错误，如果错误，下次重新连接即可
                        db.session.query(Compute).filter(Compute.token == compute.token, ).update(
                            {'last_login': datetime.datetime.now()})
                        db.session.commit()
                    except Exception as e:
                        print(e)
                else:
                    # 如果IP不可达，也在前端显示
                    logger.warning(compute.hostip + "无法连接")
                    info = {'hostname': compute.hostip, 'status': '未连接', 'message': '未连接', 'token': compute.token}
                infos.append(info)
            logger.info('宿主机信息-查询成功')
            return {'data': infos, 'message': '查询成功'}, 200
        else:
            logger.warning('宿主机信息-查询结果为空')
            return {'data': infos, 'messages': '结果为空'}, 204

    def post(self):
        """
        建立新的连接
        1. 根据参数生成 token
        2. 验证 token是否存在于数据库
        3. 不存在于数据库，校验参数
        4. 验证是否能建立连接
        5. 向数据库插入记录
        :return:
        """
        parser = reqparse.RequestParser()
        post_keys = parse_request_url_keys(request)
        for _ in post_keys:
            parser.add_argument(_)
        iargs = parser.parse_args()
        virt_connect_tokens = MD5_Strs(''.join([iargs['hostip'], iargs['user'], iargs['password']]))
        sig = compute_token_schema.validate_token(virt_connect_tokens)
        if sig == 1:
            # 如果数据库中，该连接已存在，且delete_sig为0，则返回错误信息
            logger.error(iargs['hostip'] + "该连接已存在")
            return {'message': '该连接已存在'}, 403
        else:  # 否则，尝试连接
            iargs['token'] = virt_connect_tokens
            error = compute_schema.validate(iargs)
            if error:  # 参数校验，如果参数错误，返回错误信息
                logger.error("宿主机连接参数错误")
                return {'message': str(error)}, 400
            if connection_manager.host_is_up(int(iargs['type']), iargs['hostip']) is True and isinstance(
                    connection_manager.get_connection(iargs['hostip'], iargs['user'], iargs['password'],
                                                      int(iargs['type'])), virConnect):
                # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
                vm = wvmHostDetails(iargs['hostip'], iargs['user'], iargs['password'], int(iargs['type']))
                info = vm.get_connect_info()
                info['message'] = '已连接'
                info['token'] = virt_connect_tokens
                if sig == 2:  # 如果连接已存在，但delete_sig为1，则修改delete_sig
                    try:
                        db.session.query(Compute).filter(Compute.token == virt_connect_tokens,
                                                         Compute.delete_sig == 1).update(
                            {'delete_sig': 0, 'last_login': datetime.datetime.now()})
                        db.session.commit()
                    except Exception as e:
                        # 非致命错误，可正常返回信息，下次重新连接即可
                        logger.warning(iargs['hostip'] + '数据库更新失败：' + str(e))
                elif sig == 3:  # 如果数据库内没有该记录，则尝试新增该记录
                    compute = Compute(**iargs)
                    try:
                        db.session.add(compute)
                        db.session.commit()
                    except Exception as e:
                        # 非致命错误，可正常返回信息，下次重新连接即可
                        logger.warning(iargs['hostip'] + '数据库插入失败：' + str(e))
                logger.info(iargs['hostip'] + '连接成功')
                return {'data': info, 'message': '连接成功', 'virt_connect_tokens': virt_connect_tokens}, 201
            else:
                # 如果连接失败，返回错误信息
                logger.error(iargs['hostip'] + '无法建立连接 ')
                return {'message': iargs['hostip'] + ' 无法建立连接'}, 404


class HostDisconnect(Resource):
    """
    宿主机断开连接模块
    """

    def get(self, hostname):
        token = request.headers['Authorization']
        compute = compute_schema.get_by_token(token)
        if not compute:
            logger.error('数据库查询记录为空')
            return {"message": '数据库查询记录为空'}, 403
        if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                  compute.type), virConnect):
            # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
            manager = wvmConnect(compute.hostip, compute.user, compute.password, int(compute.type))
            # 该操作是杀死libvirtd守护进程，单例
            manager.close()
        try:
            # 更新数据库
            db.session.query(Compute).filter(Compute.token == compute.token, Compute.delete_sig == 0).update(
                {'delete_sig': 1})
            db.session.commit()
            logger.info(compute.hostip + '数据库记录删除成功')
            return {'message': '删除成功'}, 204
        except Exception as e:
            logger.info(compute.hostip + '数据库记录删除失败：' + str(e))
            return {'message': '删除失败'}, 403


class HostDetail(Resource):
    """
    获取宿主机的详细信息
    """

    def get(self):
        token = request.headers['Authorization']
        compute = compute_schema.get_by_token(token)
        if not compute:
            logger.error('数据库查询记录为空')
            return {"message": '数据库查询记录为空'}, 400
        if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                  compute.type), virConnect):
            # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
            vm = wvmHostDetails(compute.hostip, compute.user, compute.password, int(compute.type))
            info = vm.get_host_detail()
            logger.info('查询成功')
            return {'data': info, 'message': '查询成功'}, 200
        else:
            logger.error("数据查询失败")
            return {'message': "数据查询失败"}, 403

class HostHistoryInfo(Resource):
    def get(self):
        history_infos = db.session.query(HistoryInfo).order_by(desc('end_time')).limit(20).all()
        history_infos = queryToDict(history_infos)
        for i in range(len(history_infos)):
            openstacks = {ip:name for ip,name in zip(history_infos[i]['openstacks_ip'].split(';'),history_infos[i]['openstacks_name'].split(';'))}
            history_infos[i]['openstacks'] = openstacks
            history_infos[i].pop('openstacks_ip')
            history_infos[i].pop('openstacks_name')
        return {'data': history_infos,'message':'查询成功'},200

class HostStoragesInfo(Resource):
    """
    根据token查询宿主机的存储信息
    """

    def get(self):
        token = request.headers['Authorization']
        compute = compute_schema.get_by_token(token)
        if not compute:
            logger.error('数据库查询记录为空')
            return {"message": '数据库查询记录为空'}, 400
        if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                  compute.type), virConnect):
            # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
            storage = wvmStorages(compute.hostip, compute.user, compute.password, int(compute.type))
            info = storage.get_storages_info()
            logger.info('查询成功')
            return {'data': info, 'message': '查询成功'}, 200
        else:
            logger.error("存储数据查询失败")
            return {'message': "存储数据查询失败"}, 403


class HostNetsInfo(Resource):
    """
    根据token查询宿主机的网络信息
    """

    def get(self):
        token = request.headers['Authorization']
        compute = compute_schema.get_by_token(token)
        if not compute:
            logger.error('数据库查询记录为空')
            return {"message": '数据库查询记录为空'}, 400
        if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                  compute.type), virConnect):
            # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
            net = wvmNetworks(compute.hostip, compute.user, compute.password, int(compute.type))
            info = net.get_networks_info()
            logger.info('网络信息查询成功')
            return {'data': info, 'message': '网络信息查询成功'}, 200
        else:
            logger.error("网络信息查询失败")
            return {'message': "网络信息查询失败"}, 403


class HostInterfacesInfo(Resource):
    """
    根据token查询宿主机的网络接口信息
    """

    def get(self):
        token = request.headers['Authorization']
        compute = compute_schema.get_by_token(token)
        if not compute:
            logger.error('数据库查询记录为空')
            return {"message": '数据库查询记录为空'}, 400
        if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                  compute.type), virConnect):
            # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
            net = wvmInterfaces(compute.hostip, compute.user, compute.password, int(compute.type))
            info = net.get_ifaces_info()
            logger.info('网络接口信息查询成功')
            return {'data': info, 'message': '网络接口信息查询成功'}, 200
        else:
            logger.error("网络接口信息查询失败")
            return {'message': "网络接口信息查询失败"}, 403


class HostNwfiltersInfo(Resource):
    """
    根据token查询宿主机的网络防火墙信息
    """

    def get(self):
        token = request.headers['Authorization']
        compute = compute_schema.get_by_token(token)
        if not compute:
            logger.error('数据库查询记录为空')
            return {"message": '数据库查询记录为空'}, 400
        if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                  compute.type), virConnect):
            # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
            nwf = wvmNWFilters(compute.hostip, compute.user, compute.password, int(compute.type))
            info = nwf.get_nwfilters_info()
            logger.info('网络防火墙信息查询成功')
            return {'data': info, 'message': '网络防火墙信息查询成功'}, 200
        else:
            logger.error("网络防火墙信息查询失败")
            return {'message': "网络防火墙信息查询失败"}, 403


class HostSecretsInfo(Resource):
    """
    根据token查询宿主机的密码信息
    """

    def get(self):
        token = request.headers['Authorization']
        compute = compute_schema.get_by_token(token)
        if not compute:
            logger.error('数据库查询记录为空')
            return {"message": '数据库查询记录为空'}, 400
        if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                  compute.type), virConnect):
            # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
            nwf = wvmConnect(compute.hostip, compute.user, compute.password, int(compute.type))
            info = nwf.get_secrets()
            logger.info('密码信息查询成功')
            return {'data': info, 'message': '密码信息查询成功'}, 200
        else:
            logger.error("密码信息查询失败")
            return {'message': "密码信息查询失败"}, 403
