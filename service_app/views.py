#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : views.py
# @Author: Cedar
# @Date  : 2019/12/11
# @Desc  :


from flask import render_template, request
from service_app import app
from service_app.controller import PageAgentManager


@app.route('/', methods=['GET', 'POST'])
def home():
    my_host = '127.0.0.1:5000'
    return render_template('home.html', my_host=my_host)


@app.route('/service_app', methods=['GET', 'POST'])
def page_agent_service():

    try:
        if request.method == 'GET':
            request_params = dict(request.args)
        else:
            request_params = dict(request.form)

        # PageAgentManager选择相对应的类，获取数据
        response = PageAgentManager(request_params).get_page_content_by_agent()

        if not response:
            response = "Failed Request! Please try again"
        return response

    except Exception as e:
        print(e)