#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   openstack.py
@Time    :   2021/6/30 11:03
@Desc    :   TODO
"""

from marshmallow import fields, Schema, validates, validates_schema, ValidationError
from models.openstack import Openstack
from . import ma


class OpenstackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Openstack
        fields = ("id_md5", "platename","auth_ip", "user_name","user_id",
            "password","domain_name","domain_id", "token","delete_sig")

    def get_by_id_md5(self, id_md5):
        openstack = Openstack.query.filter_by(id_md5=id_md5,delete_sig=0).first()
        if openstack:
            return openstack

    def get_by_auth_ip(self, auth_ip):
        openstack = Openstack.query.filter_by(auth_ip=auth_ip,delete_sig=0).first()
        if openstack:
            return openstack

    def validate_id_md5(self, id_md5):
        if Openstack.query.filter_by(id_md5=id_md5,delete_sig=0).first():
            return 1
        elif Openstack.query.filter_by(id_md5=id_md5,delete_sig=1).first():
            return 2
        else:
            return 3

    def get_all_openstacks(self):
        openstacks = Openstack.query.filter_by(delete_sig=0).all()
        if openstacks:
            return openstacks
        else:
            return []

    def get_by_token(self, token):
        openstack = Openstack.query.filter_by(token=token,delete_sig=0).first()
        if openstack:
            return openstack




openstack_schema = OpenstackSchema()
openstacks_schema = OpenstackSchema(many=True)


# class OpenstackTokenSchema(ma.Schema):
#     '''
#     Validate Compute token
#     '''
#     token = fields.Str(required=True)
#
#     @validates("token")
#     def validate_token(self, value):
#         if Compute.query.filter_by(token=value,delete_sig='N').first():
#             return 1
#         elif Compute.query.filter_by(token=value,delete_sig='Y').first():
#             return 2
#         else:
#             return 3
#
# compute_token_schema = ComputeTokenSchema()

