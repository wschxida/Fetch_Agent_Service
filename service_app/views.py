#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: Cedar
# @Date  : 2019/12/11
# @Desc  : 视图,写界面函数


from flask import render_template, request, send_file
from service_app.controller import FetchAgentManager
import os
from flask import Flask
import sys


# 创建项目对象
app = Flask(__name__)
curpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curpath)
model_path = os.path.join(curpath, "model")
sys.path.append(model_path)
# print(sys.path)


@app.route('/', methods=['GET', 'POST'])
def home():
    my_host = '107.180.91.218:5100'
    return render_template('home.html', my_host=my_host)


@app.route('/service_app', methods=['GET', 'POST'])
def fetch_agent_service():

    try:
        if request.method == 'GET':
            request_params = dict(request.args)
        else:
            request_params = dict(request.form)

        # FetchAgentManager选择相对应的类，获取数据
        response = FetchAgentManager(request_params).get_fetch_result_by_agent()

        if not response:
            response = "Failed Request! Please try again"
        return response

    except Exception as e:
        print(e)
        return str(e)


@app.route('/img/<path:img_src>')
def show_img(img_src):
    img_src = os.path.join(curpath, img_src)
    return send_file(img_src)
