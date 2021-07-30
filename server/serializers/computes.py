#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   computes.py
@Time    :   2021/6/22 13:52
@Desc    :   TODO
"""

from marshmallow import fields, Schema, validates, validates_schema, ValidationError
from models.computes import Compute
from . import ma


class ComputeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Compute
        fields = ("token", "hostip", "user", \
            "password","type", "last_login","delete_sig")

    def get_by_token(self, token):
        compute = Compute.query.filter_by(token=token,delete_sig=0).first()
        if compute:
            return compute

    def get_all_computes(self):
        computes = Compute.query.filter_by(delete_sig=0).all()
        return computes

    def get_by_hostip(self, hostip):
        compute = Compute.query.filter_by(hostip=hostip,delete_sig=0).first()
        if compute:
            return compute




compute_schema = ComputeSchema()
computes_schema = ComputeSchema(many=True)


class ComputeTokenSchema(ma.Schema):
    '''
    Validate Compute token
    '''
    token = fields.Str(required=True)

    @validates("token")
    def validate_token(self, value):
        if Compute.query.filter_by(token=value,delete_sig=0).first():
            return 1
        elif Compute.query.filter_by(token=value,delete_sig=1).first():
            return 2
        else:
            return 3

compute_token_schema = ComputeTokenSchema()




# class UserSchema(ma.SQLAlchemySchema):
    # id = ma.auto_field()
    # username = ma.auto_field()
    # phone = ma.auto_field()
    # created_time = ma.auto_field()
    # updated_time = ma.auto_field()


# class UserSchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ("id", "username", "phone", "created_time", "updated_time")

#     # # Smart hyperlinking
#     # _links = ma.Hyperlinks(
#     #     {"self": ma.URLFor("user_detail", id="<id>"), "collection": ma.URLFor("users")}
#     # )