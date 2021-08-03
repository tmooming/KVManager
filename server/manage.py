#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   manage.py
@Time    :   2021/6/4 11:13
@Desc    :   TODO
"""
from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.exceptions import HTTPException

import app as my_app


app = my_app.create_app()
manager = Manager(app)
Migrate(app, my_app.mysqldb)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    print('sa',app.url_map)
    manager.run()