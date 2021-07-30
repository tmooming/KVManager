#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   instance.py
@Time    :   2021/6/18 10:24
@Desc    :   实例信息获取
"""
import os
import re
from time import time, strftime, localtime, sleep

from sqlalchemy.util.langhelpers import md5_hex
from databases import mysqldb as db
from utils.MD5 import MD5
from utils.HTTP_Utils import (
    MD5_Strs,
    parse_request_url_keys,
    parse_request_data,
)
from vrtManager.instance import wvmInstances, wvmInstance
from vrtManager.hostdetails import wvmHostDetails
from vrtManager.connection import wvmConnect, connection_manager
from libvirt import libvirtError, virConnect
from serializers.computes import (
    compute_schema
)
from serializers.historyinfo import HistoryInfoSchema
from models.historyinfo import HistoryInfo
from models.uploadimage import UploadImage
from serializers.uploadimage import uploadimage_schema
from flask import request
from flask_restful import (
    reqparse,
    Resource
)
from flask import session

import logging
import sys

sys.path.append("../..")

logger = logging.getLogger("instance")
# 镜像准备状态信息存储
image_status_info = {"start_time": 0, "step": 0, "status": "start", "message": "准备"}


class InstancesInfo(Resource):
    """
    根据token获取当前宿主机下的所有实例简要信息
    """

    def get(self):
        token = request.headers["Authorization"]
        compute = compute_schema.get_by_token(token)
        if not compute:
            logger.error("数据库查询记录为空")
            return {"message": "数据库查询记录为空"}, 400
        if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                  compute.type), virConnect):
            # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
            instance = wvmInstances(
                compute.hostip, compute.user, compute.password, int(compute.type))
            info = instance.get_instances_info()
            logger.info("实例信息查询成功")
            return {"data": info, "message": "实例信息查询成功"}, 200
        else:
            logger.error(compute.hostip + "连接失败")
            return {"message": compute.hostip + "连接失败"}, 403


class InstanceInfo(Resource):
    """
    根据宿主机和实例名称，获得某个实例的简要信息
    """

    def get(self, name):
        token = request.headers["Authorization"]
        compute = compute_schema.get_by_token(token)
        if not compute:
            logger.error("数据库查询记录为空")
            return {"message": "数据库查询记录为空"}, 400
        if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                  compute.type), virConnect):
            # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
            connect = wvmConnect(compute.hostip, compute.user, compute.password, 1)
            info = connect.get_user_instances(name)
            logger.info("实例信息查询成功")
            return {"data": info, "message": "实例信息查询成功"}, 200
        else:
            logger.error(compute.hostip + "连接失败")
            return {"message": compute.hostip + "连接失败"}, 403


class InstanceStatusControl(Resource):
    """
    对某个实例的生命周期进行控制
    """

    def post(self, name):
        parser = reqparse.RequestParser()
        post_keys = parse_request_url_keys(request)
        token = request.headers["Authorization"]
        # for _ in post_keys:
        #     parser.add_argument(_)
        # iargs = parser.parse_args()
        iargs = post_keys
        compute = compute_schema.get_by_token(token)
        if not compute:
            logger.error("数据库查询记录为空")
            return {"message": "数据库查询记录为空"}, 400
        if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                  compute.type), virConnect):
            # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
            instance = wvmInstances(
                compute.hostip, compute.user, compute.password, int(compute.type))
            try:
                if iargs["method"] == "start":
                    instance.start(name)
                elif iargs["method"] == "powercycle":
                    instance.force_shutdown(name)
                    instance.start(name)
                elif iargs["method"] == "suspend":
                    instance.suspend(name)
                elif iargs["method"] == "resume":
                    instance.resume(name)
                elif iargs["method"] == "poweroff":
                    instance.shutdown(name)
                    start_time = time()
                    while instance.get_instance_status(name)!='shut off' and time() - start_time < 60:
                        sleep(1)
                    if instance.get_instance_status(name)!='shut off':
                        instance.force_shutdown(name)
                elif iargs["method"] == "force_off":
                    instance.force_shutdown(name)
                else:
                    print(iargs["method"])
            except libvirtError as e:
                logger.error("实例" + name + iargs["method"] + "失败")
                return {"message": "实例" + name + iargs["method"] + "失败"}, 403
            finally:
                status = instance.get_instance_status(name)
            logger.info("实例" + name + iargs["method"] + "成功")
            return {"message": "实例" + name + iargs["method"] + "成功", "status": status}, 201
        else:
            logger.error(compute.hostip + "连接失败")
            return {"message": compute.hostip + "连接失败"}, 403


class InstanceImageInfo(Resource):
    """
    获取某个镜像的image信息
    """

    def get(self, name):
        token = request.headers["Authorization"]
        compute = compute_schema.get_by_token(token)
        if not compute:
            logger.error("数据库查询记录为空")
            return {"message": "数据库查询记录为空"}, 400
        if connection_manager.host_is_up(compute.type, compute.hostip) is True and isinstance(
                connection_manager.get_connection(compute.hostip, compute.user, compute.password,
                                                  compute.type), virConnect):
            # 判断该IP的目标端口是否可连接，同时libvirtd服务是否可用
            instance = wvmInstance(compute.hostip, compute.user,
                                   compute.password, int(compute.type), name)
            disc = instance.get_disk_devices()
            logger.info("实例 " + name + " disc信息获取成功")
            return {"data": disc, "message": "实例" + name + "disc信息获取成功"}, 200
        else:
            logger.error(compute.hostip + "连接失败")
            return {"message": compute.hostip + "连接失败"}, 403


class InstanceImageUpload(Resource):
    def __init__(self) -> None:
        self.md5 = MD5()
        self.md5.register(self)

    def update_message(self, message):
        # 观察者模式，实时获取文件拷贝和MD5生成时 image_status_info的变化
        global image_status_info
        image_status_info = {"start_time": time(), "step": 1, "status": "copy", "message": message}

    def post(self, name):
        global image_status_info
        parser = reqparse.RequestParser()
        post_keys = parse_request_data(request)
        # for _ in post_keys:
        #     parser.add_argument(_)
        # print(parser[""])
        # iargs = parser.parse_args()
        # 暂时不做参数校验
        iargs = post_keys
        token = request.headers["Authorization"]
        history_info = {'start_time': strftime("%Y/%m/%d %H:%M:%S", localtime()),
                       'custom_ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                       'host_ip': request.host.split(':')[0],'action':'','image_name':iargs['image_name']}
        image_status_info = {"start_time": time(), "step": 1, "status": "prepare", "message": "准备"}
        # 1. 判断image-upload是否存在该文件
        image_runing_prex_dir, image_file_name = iargs["image_path"].rsplit("/", 1)
        image_upload_prex_dir = image_runing_prex_dir.replace("image-running", "image-upload")
        # image_runing_prex_dir, image_file_name = "/vmdata/image-running", "ubuntu18.04-x64-test.raw"
        # image_upload_prex_dir = image_runing_prex_dir.replace("image-running", "image-upload")
        if os.path.isfile(image_upload_prex_dir + "/" + image_file_name):
            # 1.1.1 计算image-upload中该文件的md5值
            current_md5 = self.md5.GetFileMd5(image_upload_prex_dir + "/" + image_file_name)
            # 1.1.2 在数据库中查找是否存在running_md5与upload_md5均等于该md5值的记录,且时间间隔为24小时，如果相等，则直接上传image
            upload_image = uploadimage_schema.get_by_time_and_md5(
                upload_md5=current_md5, time_interval=24)
            if upload_image:
                logger.info(name + "上传就绪")
                image_status_info = {"start_time": time(), "step": 1, "status": "finish", "message": "上传就绪"}
                history_info['action']='计算文件MD5值完成'
                return {"data": {"upload_md5": current_md5, 'history_info':history_info},
                        "message": "上传就绪"}, 200
            elif uploadimage_schema.get_by_upload_md5(upload_md5=current_md5):
                # 如果存在24小时前的记录，则将前一条记录逻辑删除
                db.session.query(UploadImage).filter(UploadImage.running_md5 == current_md5,
                                                     UploadImage.upload_md5 == current_md5,
                                                     UploadImage.delete_sig == 0).update(
                    {"delete_sig": 1})
                db.session.commit()
                db.session.close()
        # 1.2 如果image-upload中不存在该文件，则先需要关机
        compute = compute_schema.get_by_token(token)
        instance = wvmInstances(
            compute.hostip, compute.user, compute.password, int(compute.type))
        base_status = status = instance.get_instance_status(name)
        start_time = time()
        # 1.2.1 首先确保实例处于关机状态
        while status != "shut off" and time() - start_time < 60:
            # 如果没有关机，且尝试关机时间小于60秒
            try:
                if status == "running":
                    instance.shutdown(name)
                elif status == "paused":
                    instance.force_shutdown(name)
            except Exception as e:
                instance.force_shutdown(name)
            finally:
                status = instance.get_instance_status(name)
                image_status_info = {"start_time": time(), "step": 1, "status": status, "message": "关机中"}
        if status != "shut off":
            # 1.2.2 如果关机失败，返回报错信息
            image_status_info = {"start_time": time(), "step": 1, "status": "error", "message": "关机失败"}
            history_info['action'] += ';' + name+'关机失败'
            history_info['status'] = '失败'
            db.session.add(HistoryInfo(**history_info))
            db.session.commit()
            return {"message": "关机失败，请手动关机"}, 400
        # 1.2.3 关机成功后，再检查image-upload中是否有同名文件
        if os.path.isfile(image_upload_prex_dir + "/" + image_file_name):
            temp_name = image_file_name + MD5_Strs(image_file_name)
        else:
            temp_name = image_file_name
        # 1.2.4 将image-running中的文件复制到image-running中，并同时计算md5值
        copy_start_time = time()
        image_status_info = {"start_time": copy_start_time, "step": 1, "status": "copy", "message": "文件拷贝中"}
        running_md5, upload_md5 = self.md5.GetFileMd5AandCopy(
            image_runing_prex_dir + "/" + image_file_name, image_upload_prex_dir + "/" + temp_name)
        if running_md5 == upload_md5:
            # 1.2.5 如果复制成功，则将拷贝后的文件改名
            if temp_name != image_file_name:
                os.rename(image_upload_prex_dir + "/" + image_file_name,
                          image_upload_prex_dir + "/" + image_file_name + "." + strftime("%Y_%m_%d_%H_%M_%S",
                                                                                         localtime()))
                os.rename(image_upload_prex_dir + "/" + temp_name, image_upload_prex_dir + "/" + image_file_name)
            image_status_info = {"start_time": copy_start_time, "step": 1, "status": "finish", "message": "文件拷贝完成"}
            upload_image = UploadImage(**{"running_md5": running_md5, "upload_md5": upload_md5,
                                          "image_path": image_upload_prex_dir + "/" + image_file_name})
            db.session.add(upload_image)
            db.session.commit()
            # 1.2.6 将instance恢复原状
            if base_status != status:
                instance.start(name)
            image_status_info = {"start_time": copy_start_time, "step": 1, "status": "finish", "message": "上传就绪"}
            history_info['action'] += ';' + '文件拷贝完成'
            return {"data": {"upload_md5": upload_md5,'history_info':history_info}, "message": "上传就绪"}, 200
        else:
            image_status_info = {"start_time": copy_start_time, "step": 1, "status": "error", "message": "文件拷贝失败"}
            history_info['action'] += ';' + name + '文件拷贝失败'
            history_info['status'] = '失败'
            db.session.add(HistoryInfo(**history_info))
            db.session.commit()
            return {"message": "请重试"}, 400

    def get(self, name):
        return {"message": "ok" + name}, 200


class InstanceUploadPrepareInfo(Resource):
    def get(self):
        return {"data": image_status_info, "message": "返回成功"}, 200


class InstanceDetail(Resource):
    """
    获取某个实例的详细信息
    """

    def get(self):
        token = request.headers["Authorization"]
        compute = compute_schema.get_by_token(token)
        instances = wvmInstances(
            compute.hostip, compute.user, compute.password, int(compute.type))
        info = instances.get_instances_info()
        return {"data": info, "message": "请求成功"}, 200

    def post(self):
        print(session)
        return {"message": "结果"}, 201


class InstanceResizeCMD(Resource):
    """
    更改某个实例的CPU、内存、磁盘大小
    """

    def get(self, name):
        token = request.headers["Authorization"]
        compute = compute_schema.get_by_token(token)
        vm = wvmHostDetails(compute.hostip, compute.user,
                            compute.password, int(compute.type))
        instance = wvmInstance(compute.hostip, compute.user,
                               compute.password, int(compute.type), name)
        info = {}
        info["host_cpu"] = int(vm.wvm.getInfo()[2])
        info["cur_vcpu"] = int(instance.get_cur_vcpu())
        info["vcpu"] = int(instance.get_vcpu())
        info["vcpu_range"] = [i for i in range(1, info["host_cpu"] + 1)]
        info["host_memory"] = vm.get_memory_usage()["total"]
        info["cur_memory"] = instance.get_cur_memory()
        info["memory"] = instance.get_memory()
        info["memory_range"] = [i for i in range(
            256, 1024, 256)] + [i for i in range(1024, int(info["host_memory"] + 1), 1024)]
        info["disk"] = instance.get_disk_devices()
        return {"data": info, "message": "请求成功"}, 200

    def post(self, name):
        parser = reqparse.RequestParser()
        post_keys = parse_request_url_keys(request)
        token = request.headers["Authorization"]
        for _ in post_keys:
            parser.add_argument(_)
        iargs = parser.parse_args()
        compute = compute_schema.get_by_token(token)
        instance = wvmInstance(compute.hostip, compute.user,
                               compute.password, int(compute.type), name)
        try:
            if iargs["method"] == "resize_cpu":
                instance.resize_cpu(
                    cur_vcpu=iargs["cur_vcpu"], vcpu=iargs["vcpu"])
            elif iargs["method"] == "resize_mem":
                instance.resize_mem(cur_memory=int(
                    iargs["cur_memory"]), memory=int(iargs["memory"]))
            elif iargs["method"] == "resize_disk":
                print(iargs["disks[]"])
        except libvirtError as e:
            return {"message": "修改失败"}, 403
        return {"message": "更改成功"}, 204
