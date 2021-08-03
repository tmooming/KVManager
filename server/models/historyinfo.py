#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   historyinfo.py
@Time    :   2021/7/28 17:47
@Desc    :   history_info数据表
"""


from databases import mysqldb as db
from sqlalchemy.sql import func


class HistoryInfo(db.Model):
    print('ssssssss')
    __tablename__ = 'history_info'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    custom_ip = db.Column(
        db.String(16),
        nullable=False
    )
    host_ip = db.Column(
        db.String(16),
        nullable=False
    )
    openstacks_name = db.Column(
        db.String(300),
        nullable=True
    )
    openstacks_ip = db.Column(
        db.String(300),
        nullable=True
    )
    image_name = db.Column(
        db.String(100),
        nullable=True
    )
    checksum = db.Column(
        db.String(32),
        nullable=True
    )
    action = db.Column(
        db.String(400),
        nullable=True
    )
    status = db.Column(
        db.String(10),
        nullable=True
    )
    start_time = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    end_time = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=func.now()
    )

    # __mapper_args__ = {
    #     "order_by": created_time
    # }

    def __repr__(self):
        return f'<HistoryInfo {self.id}>'

