#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : runserver.py
# @Author: Cedar
# @Date  : 2019/12/11
# @Desc  :

from service_app.views import app


if __name__ == '__main__':
    app.run('0.0.0.0', port='5101', debug=True, threaded=True)



