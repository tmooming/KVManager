"""
    *************************** 
    --------description-------- 
 	 Description: 
 	 Version: 1.0
 	 Autor: Tu Ruwei
 	 Date: 2021-07-08 16:13:32
 	 LastEditors: Tu Ruwei
 	 LastEditTime: 2021-07-08 17:08:45

    ***************************  
"""

from databases import mysqldb as db
from sqlalchemy.sql import func


class UploadImage(db.Model):

    __tablename__ = 'upload_image'

    
 
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    running_md5 = db.Column(
        db.String(32),
        unique=True
    )
    upload_md5 = db.Column(
        db.String(32),
        unique=True
    )
    image_path = db.Column(
        db.String(200),
        nullable=True
    )
    create_time = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True,
        default=func.now()
    )
    delete_sig = db.Column(
        db.SmallInteger,
        default=0
    )
    # __mapper_args__ = {
    #     "order_by": created_time
    # }

    def __repr__(self):
        return f'<UploadImage {self.id}>'


