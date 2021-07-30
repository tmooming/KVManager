"""
    *************************** 
    --------description-------- 
 	 Description: 
 	 Version: 1.0
 	 Autor: Tu Ruwei
 	 Date: 2021-07-08 16:13:33
 	 LastEditors: Tu Ruwei
 	 LastEditTime: 2021-07-08 17:15:11

    ***************************  
"""
from datetime import datetime,timedelta
from marshmallow import fields, Schema, validates, validates_schema, ValidationError
from models.uploadimage import UploadImage
from . import ma


class UploadImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UploadImage
        fields = ("id","running_md5","upload_md5", "image_path","create_time", "delete_sig")

    def get_by_unique_md5(self, running_md5,upload_md5):
        uploadimage = UploadImage.query.filter_by(running_md5=running_md5,upload_md5=upload_md5,delete_sig=0).first()
        if uploadimage:
            return uploadimage
    
    def get_by_time_and_md5(self,upload_md5,time_interval):
        now = datetime.now()
        time_interval = now - timedelta(hours=time_interval)
        uploadimage = UploadImage.query.filter(UploadImage.create_time > time_interval).filter_by(
            running_md5=upload_md5,upload_md5=upload_md5,delete_sig=0).first()
        if uploadimage:
            return uploadimage

    def get_by_upload_md5(self,upload_md5):
        uploadimage = UploadImage.query.filter_by(running_md5=upload_md5,upload_md5=upload_md5,delete_sig=0).first()
        if uploadimage:
            return uploadimage

    def validate_unique_md5(self, running_md5,upload_md5):
        if UploadImage.query.filter_by(running_md5=running_md5,upload_md5=upload_md5,delete_sig=0).first():
            return True


uploadimage_schema = UploadImageSchema()

