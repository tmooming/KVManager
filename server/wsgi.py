"""
    *************************** 
    --------description-------- 
 	 Description: 
 	 Version: 1.0
 	 Autor: Tu Ruwei
 	 Date: 2021-07-13 17:18:43
 	 LastEditors: Tu Ruwei
 	 LastEditTime: 2021-07-14 15:41:21

    ***************************  
"""
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   TURW
@Contact :   tmooming@163.com
@Software:   PyCharm
@File    :   wsgi.py
@Time    :   2021/6/4 13:37
@Desc    :   TODO
"""

# deploy production
# gunicorn -w 4 -b 0.0.0.0:5000 -k wsgi:create_app
import sys
from app import create_app
my_app = create_app(configName='production')

if __name__ == "__main__":
	my_app.run()