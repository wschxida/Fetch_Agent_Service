#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : get_common_friend_by_twiangulate.py
# @Author: Cedar
# @Date  : 2020/10/14
# @Desc  :


from lxml import etree
import os
import time
import platform
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


driver = None
old_height = 0
curpath = os.path.dirname(os.path.realpath(__file__))
driver_path = os.path.join(curpath, "..", "..", "..")


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


def start_selenium(user_data_dir):
    global driver

    options = Options()
    #  Code to disable notifications pop up of Chrome Browser
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
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
    # 取一个chrome user-data-dir目录，每个目录的Chromedriver是互相隔开的，登录不同的账号
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    options.add_argument(r"user-data-dir=" + user_data_dir)
    print(user_data_dir)

    # 打开chrome人工登录账号
    # google-chrome --user-data-dir="/home/kismanager/KIS/selenium/Twitter"
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    try:
        platform_ = platform.system().lower()
        if platform_ in ['linux', 'darwin']:
            options.add_argument('--headless')  # 浏览器不提供可视化页面
            chromedriver_path = os.path.join(driver_path, "chromedriver")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        else:
            user_data_dir = 'E:\\selenium\\AutomationProfile1'
            options.add_argument(r"user-data-dir=" + user_data_dir)
            chromedriver_path = os.path.join(driver_path, "chromedriver.exe")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    except Exception as e:
        print(e)

    driver.implicitly_wait(60)  # 隐性等待，最长等30秒
    driver.set_page_load_timeout(120)   # 设置页面加载超时
    driver.set_script_timeout(120)   # 设置页面异步js执行超时
    # driver.maximize_window()


def get_common_friend_by_twiangulate(url, user_data_dir):

    author_list = []
    try:
        start_selenium(user_data_dir)
        driver.get(url)
        time.sleep(2)
        page_source = driver.page_source
        driver.close()
        # 使用etree来xpath切割，减少报错信息
        root = etree.HTML(page_source, parser=etree.HTMLParser(encoding='utf-8'))
        items = root.xpath('//table[@id="result_list"]//tr')
        for item in items:
            # 不要写item.xpath('.//a[@class="person_link"]/text()')[0]，有可能导致list out of index
            # author_id页面上没有
            # author_id = ""
            author_account = "".join(item.xpath('./td[2]/@data-sort'))
            author_name = ""
            author_url = 'https://twitter.com/' + author_account
            author_img_url = "".join(item.xpath('./td[2]//img/@src'))
            author_description = "".join(item.xpath('./td[3]//text()'))
            author_following_count = "".join(item.xpath('./td[4]/@data-sort'))
            author_follower_count = "".join(item.xpath('./td[5]/@data-sort'))
            author_message_count = ""

            author_item = {
                # "author_id": author_id,
                "author_account": author_account,
                "author_name": author_name,
                "author_url": author_url,
                "author_img_url": author_img_url,
                "author_description": author_description,
                "author_follower_count": author_follower_count,
                "author_following_count": author_following_count,
                "author_message_count": author_message_count,
            }
            if len(author_account) > 0:
                author_list.append(author_item)

    except Exception as e:
        driver.close()
        print(e)
        return str(e)

    return author_list


def main():
    url = 'http://www.twiangulate.com/search/BillGates-Oprah/common_friends/table/my_friends-1/'
    # user_data_dir = 'E:\\selenium\\AutomationProfile1'
    user_data_dir = '/home/kismanager/KIS/selenium/Twitter'
    result = get_common_friend_by_twiangulate(url, user_data_dir)
    print(result)


if __name__ == '__main__':
    main()
