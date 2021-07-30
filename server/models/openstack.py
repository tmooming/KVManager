#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   openstack.py
@Time    :   2021/6/30 10:56
@Desc    :   openstack数据表
"""


from databases import mysqldb as db
from sqlalchemy.sql import func


class Openstack(db.Model):

    __tablename__ = 'openstack'

    id_md5 = db.Column(
        db.String(32),
        primary_key=True
    )
    platename = db.Column(
        db.String(100),
        nullable=True
    )
    auth_ip = db.Column(
        db.String(16),
        unique=True,
        nullable=False
    )
    user_name = db.Column(
        db.String(45),
        nullable=True
    )
    user_id = db.Column(
        db.String(32),
        nullable=True
    )
    password = db.Column(
        db.String(45),
        nullable=True
    )
    domain_name = db.Column(
        db.String(45),
        nullable=True
    )
    domain_id = db.Column(
        db.String(32),
        nullable=True
    )
    token = db.Column(
        db.String(200),
        nullable=True
    )
    delete_sig = db.Column(
        db.SmallInteger,
        default=0
    )

    # __mapper_args__ = {
    #     "order_by": created_time
    # }

    def __repr__(self):
        return f'<Openstack {self.id_md5}>'

