#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extractor_get_author_retweet_the_target_tweet.py
# @Author: Cedar
# @Date  : 2019/12/31
# @Desc  :


import html
import json
import re

import os
import time
import platform
import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


driver = None
old_height = 0
curpath = os.path.dirname(os.path.realpath(__file__))
driver_path = os.path.join(curpath, "..")


def check_height():
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


def scroll(total_scrolls=5, scroll_time=10):
    global old_height
    current_scrolls = 0
    total_scrolls = int(total_scrolls)

    while True:
        try:
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, scroll_time, 5).until(lambda driver: check_height())
            current_scrolls += 1
        except TimeoutException:
            break
    return


def start_selenium(user_data_dir_list):
    global driver

    options = Options()
    #  Code to disable notifications pop up of Chrome Browser
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    options.add_argument('--headless')  # 浏览器不提供可视化页面
    # twitter下面这个会导致登录失败
    # options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    options.add_argument('--audio-output-channels=0')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-translate')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-sync')
    # options.add_argument("--disable-javascript")    # 禁用JavaScript
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('--no-sandbox')  # 以最高权限运行,解决DevToolsActivePort文件不存在的报错
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 隐藏window.navigator.webdriver
    # 随机取一个chromedriver目录，每个目录的Chromedriver是互相隔开的，登录不同的账号，每次启动随机分配
    index = random.randint(0, len(user_data_dir_list) - 1)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # user_data_dir_arg = r"user-data-dir=" + user_data_dir[index]
    user_data_dir_arg = r"user-data-dir=" + user_data_dir_list[0]
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    options.add_argument(user_data_dir_arg)
    print(user_data_dir_arg)
    # print(index)
    # return user_data_dir_arg

    try:
        platform_ = platform.system().lower()
        if platform_ in ['linux', 'darwin']:
            chromedriver_path = os.path.join(driver_path, "chromedriver")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        else:
            chromedriver_path = os.path.join(driver_path, "chromedriver.exe")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    except:
        print("Kindly replace the Chrome Web Driver with the latest one from"
              "http://chromedriver.chromium.org/downloads"
              "\nYour OS: {}".format(platform_)
              )

    driver.set_page_load_timeout(60)   # 设置页面加载超时
    driver.set_script_timeout(60)   # 设置页面异步js执行超时
    driver.maximize_window()

    # 先走twitter首页，再滑动一下，模拟人工操作
    driver.get("https://www.twitter.com/")
    time.sleep(5)
    scroll(1)
    time.sleep(2)

    # # 如果发现没登录，就退出
    # try:
    #     is_not_login = driver.find_element_by_name('email')
    #     if is_not_login:
    #         return "NotLogin"
    #     #     email = eval(twitter_email_password[index])["email"]
    #     #     password = eval(twitter_email_password[index])["password"]
    #     #     print(email)
    #     #     login(email, password)
    #     #     driver.get(url)
    # except Exception as e:
    #     return None


def login(email, password):
    """ Logging into our own profile """

    driver.get("https://twitter.com/login")
    driver.maximize_window()

    # filling the form
    driver.find_element_by_name('session[username_or_email]').send_keys(email)
    driver.find_element_by_name('session[password]').send_keys(password)

    # clicking on login button
    try:
        driver.find_element_by_class('submit EdgeButton EdgeButton--primary EdgeButtom--medium').click()
    except Exception as e:
        pass


def extractor_get_author_retweet_the_target_tweet(target_tweet_url, user_data_dir_list):

    url = target_tweet_url + '/retweets'
    # url = 'https://twitter.com/BBC/status/1214955182775246850/retweets'
    # user_data_dir_list = ['E:\\selenium\\AutomationProfile1']
    author_list = []
    status = '0'

    try:
        start_selenium(user_data_dir_list)
        driver.get(target_tweet_url)
        time.sleep(3)
        driver.get(url)
        time.sleep(5)
        # scroll(5)
        items = driver.find_elements_by_xpath('//div[@aria-label="Timeline: Retweeted by"]/div/div/div')
        status = '1'
        for item in items:
            author_id = item.find_elements_by_xpath('.//div[contains(@data-testid,"-follow")]')[0].get_attribute('data-testid')
            author_id = author_id.replace('-follow', '')
            author_account = item.find_elements_by_xpath('.//span[contains(text(),"@")]')[0].text
            author_account = author_account[1:]  # 去掉开头的@符号
            author_name = item.find_elements_by_xpath('.//span')[0].text
            author_url = 'https://twitter.com/' + author_account
            author_img_url = item.find_elements_by_xpath('.//img')[0].get_attribute('src')

            author_item = {
                "author_id": author_id,
                "author_account": author_account,
                "author_name": author_name,
                "author_url": author_url,
                "author_img_url": author_img_url,
            }
            author_list.append(author_item)

    except Exception as e:
        status = str(e)
        print(e)

    result = {"status": status, "agent_type": "twitter", "fetch_type": "get_author_retweet_the_target_tweet",
              "data": author_list}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    driver.close()
    return html_result


def main():
    target_tweet_url = 'https://twitter.com/BBC/status/1214955182775246850'
    user_data_dir_list = ['E:\\selenium\\AutomationProfile1']
    result = extractor_get_author_retweet_the_target_tweet(target_tweet_url, user_data_dir_list)
    print(result)


if __name__ == '__main__':
    main()
