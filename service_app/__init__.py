#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : __init__.py
# @Author: Cedar
# @Date  : 2019/12/11
# @Desc  :

from flask import Flask

# 创建项目对象
app = Flask(__name__)
import service_app.views

