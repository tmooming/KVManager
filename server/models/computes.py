#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   computes.py
@Time    :   2021/6/22 13:10
@Desc    :   宿主机信息
"""


from databases import mysqldb as db
from sqlalchemy.sql import func


class Compute(db.Model):

    __tablename__ = 'computes'

    token = db.Column(
        db.String(32),
        primary_key=True
    )
    hostip = db.Column(
        db.String(16),
        unique=True,
        nullable=False
    )
    user = db.Column(
        db.String(20),
        nullable=True
    )
    password = db.Column(
        db.String(20),
        nullable=True
    )
    type = db.Column(
        db.SmallInteger,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=func.now()
    )
    delete_sig = db.Column(
        db.SmallInteger,
        nullable=False,
        default=0
    )

    # __mapper_args__ = {
    #     "order_by": created_time
    # }

    def __repr__(self):
        return f'<Compute {self.token}>'
