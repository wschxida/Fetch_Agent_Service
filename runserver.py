#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : runserver.py
# @Author: Cedar
# @Date  : 2019/12/11
# @Desc  :


from service_app.views import app
from flask_script import Manager, Shell


manager = Manager(app)

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()

# 以server形式运行
# start python runserver.py runserver --host 0.0.0.0 --port 5001
# start python runserver.py runserver --host 0.0.0.0 --port 5002
# start python runserver.py runserver --host 0.0.0.0 --port 5003
# start python runserver.py runserver --host 0.0.0.0 --port 5004
# start python runserver.py runserver --host 0.0.0.0 --port 5005
