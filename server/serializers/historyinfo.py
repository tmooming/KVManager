#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   historyinfo.py
@Time    :   2021/7/28 17:56
@Desc    :   TODO
"""
from datetime import datetime, timedelta
from marshmallow import fields, Schema, validates, validates_schema, ValidationError
from models.historyinfo import HistoryInfo
from . import ma


class HistoryInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistoryInfo
        fields = ("id", "custom_ip", "host_ip", "openstacks_name","openstacks_ip","image_name","checksum", "action","status","start_time","end_time")

    def get_by_custom_ip(self, custom_ip):
        historyinfos = HistoryInfo.query.filter_by(custom_ip=custom_ip).all()
        if historyinfos:
            return historyinfos

    def get_by_time(self, time_interval):
        now = datetime.now()
        time_interval = now - timedelta(hours=time_interval)
        history_infos = HistoryInfo.query.filter(HistoryInfo.end_time > time_interval).all()
        if history_infos:
            return history_infos




historyinfo_schema = HistoryInfoSchema()

