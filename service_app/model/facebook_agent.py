# encoding=utf-8

import platform
import configparser
import os
import time
import random
import json
import html
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from service_app.model.base import BasePageAgent

# Global Variables
# 用os模块来读取
curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "config_param.ini")  # 读取到本机的配置文件
# 调用读取配置模块中的类
conf = configparser.RawConfigParser()
conf.read(cfgpath, encoding="utf-8")
# 调用get方法，然后获取配置的数据
profile_url_pattern = conf.get("facebook", "profile_url_pattern")
message_url_pattern = conf.get("facebook", "message_url_pattern")
friend_url_pattern = conf.get("facebook", "friend_url_pattern")
total_scrolls_default = int(conf.get("scroll", "total_scrolls_default"))
scroll_time = int(conf.get("scroll", "scroll_time"))
user_data_dir = conf.get("chromedriver", "user_data_dir")
# 转成list
if user_data_dir:
    user_data_dir = user_data_dir.split("||")

facebook_email_password = conf.get("login", "facebook_email_password")
# 转成list
if facebook_email_password:
    facebook_email_password = facebook_email_password.split("||")

driver = None
current_scrolls = 0
old_height = 0


# =============================================================================


def check_height():
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


# helper function: used to scroll the page
def scroll(total_scrolls=total_scrolls_default):
    global old_height
    current_scrolls = 0
    # 如果传入total_scrolls为空，则用默认值；如果不传，也用默认值
    if not total_scrolls:
        total_scrolls = total_scrolls_default

    # print(total_scrolls)
    total_scrolls = int(total_scrolls)

    while (True):
        try:
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # WebDriverWait(driver, scroll_time, 0.05).until(lambda driver: check_height())
            WebDriverWait(driver, scroll_time, 5).until(lambda driver: check_height())
            current_scrolls += 1
        except TimeoutException:
            break

    return


def start_selenium(url):
    global driver

    options = Options()

    #  Code to disable notifications pop up of Chrome Browser
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    # options.add_argument('--headless')  # 浏览器不提供可视化页面
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # options.add_argument("allow-file-access-from-files")
    # options.add_argument("use-fake-device-for-media-stream")
    # options.add_argument("use-fake-ui-for-media-stream")
    # options.add_argument("use-file-for-fake-audio-capture=C:\\PATH\\TO\\WAV\\xxx.wav")
    options.add_argument('--audio-output-channels=0')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-translate')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-sync')
    # option.add_argument("--disable-javascript")    # 禁用JavaScript
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('--no-sandbox')  # 以最高权限运行,解决DevToolsActivePort文件不存在的报错
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 隐藏window.navigator.webdriver
    # 随机取一个chromedriver目录，每个目录的Chromedriver是互相隔开的，登录不同的账号，每次启动随机分配
    index = random.randint(0, len(user_data_dir) - 1)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # user_data_dir_arg = r"user-data-dir=" + user_data_dir[index]
    user_data_dir_arg = r"user-data-dir=" + user_data_dir[0]
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    options.add_argument(user_data_dir_arg)
    print(user_data_dir_arg)
    # print(index)
    # return user_data_dir_arg

    try:
        platform_ = platform.system().lower()
        if platform_ in ['linux', 'darwin']:
            chromedriver_path = os.path.join(curpath, "chromedriver")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        else:
            chromedriver_path = os.path.join(curpath, "chromedriver.exe")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    except:
        print("Kindly replace the Chrome Web Driver with the latest one from"
              "http://chromedriver.chromium.org/downloads"
              "\nYour OS: {}".format(platform_)
              )

    driver.set_page_load_timeout(60)   # 设置页面加载超时
    driver.set_script_timeout(60)   # 设置页面异步js执行超时
    driver.maximize_window()

    # 先走Facebook首页，再滑动一下，模拟人工操作
    driver.get("https://www.facebook.com/")
    time.sleep(2)
    scroll(1)
    time.sleep(3)
    driver.get(url)
    time.sleep(5)
    # 如果发现没登录，就退出
    try:
        is_not_login = driver.find_element_by_name('email')
        if is_not_login:
            return "NotLogin"
        #     email = eval(facebook_email_password[index])["email"]
        #     password = eval(facebook_email_password[index])["password"]
        #     print(email)
        #     login(email, password)
        #     driver.get(url)
    except Exception as e:
        return None


def login(email, password):
    """ Logging into our own profile """

    driver.get("https://en-gb.facebook.com")
    driver.maximize_window()

    # filling the form
    driver.find_element_by_name('email').send_keys(email)
    driver.find_element_by_name('pass').send_keys(password)

    # clicking on login button
    try:
        driver.find_element_by_name('login').click()
    except Exception as e:
        pass

    try:
        driver.find_element_by_id('loginbutton').click()
    except Exception as e:
        pass


def create_original_link(url):
    if url.find(".php") != -1:
        original_link = "https://en-gb.facebook.com/" + ((url.split("="))[1])

        if original_link.find("&") != -1:
            original_link = original_link.split("&")[0]

    elif url.find("fnr_t") != -1:
        original_link = "https://en-gb.facebook.com/" + ((url.split("/"))[-1].split("?")[0])
    elif url.find("_tab") != -1:
        original_link = "https://en-gb.facebook.com/" + (url.split("?")[0]).split("/")[-1]
    else:
        original_link = url

    return original_link


def get_middle_str(content, start_str, end_str):
    """通用函数，获取前后两个字符串中间的内容"""
    try:
        start_index = content.index(start_str)
        if start_index >= 0:
            start_index += len(start_str)
        content = content[start_index:]
        end_index = content.index(end_str)
        return content[:end_index]
    except Exception as e:
        print(e)


def get_author_id(content):
    user_id = get_middle_str(content, '"entity_id":"', '"')
    page_id = get_middle_str(content, '"pageID":"', '"')

    if user_id:
        author_id = user_id
    else:
        author_id = page_id

    return author_id


def get_author_account(content):
    user_account = get_middle_str(content, '"uri":"', '"')
    page_account = get_middle_str(content, '"username":"', '"')
    print(user_account)

    if page_account:
        author_account = page_account

    else:
        user_account = user_account + "#"
        author_account = get_middle_str(user_account, 'facebook.com\/', '#')
        if not author_account.find("profile.php") == -1:
            author_account = ''

    return author_account


def get_author_name(content):
    user_name = get_middle_str(content, '<title id="pageTitle">', '</title>')
    page_name = get_middle_str(content, '"pageName":"', '"')

    if user_name:
        author_name = user_name
    else:
        author_name = page_name

    return author_name


def get_author_profile_image(driver):
    try:
        user_profile_image = driver.find_elements_by_xpath('//a[contains(@class,"profilePicThumb")]/img')
        page_profile_image = driver.find_elements_by_xpath('//a[contains(@aria-label,"Profile picture")]/div/img')

        if user_profile_image:
            author_profile_image = user_profile_image[0].get_attribute('src')
        else:
            author_profile_image = page_profile_image[0].get_attribute('src')

        return author_profile_image
    except:
        pass


class FacebookAgent(BasePageAgent):
    """
    facebook类，获取profile，message, friend
    调用get_page_content_by_request可根据page_type返回相应结果
    """

    def __init__(self, params):
        BasePageAgent.__init__(self, params)
        # target参数是Facebook独有，表示account或者id都可以
        if self.target_account:
            self.target = self.target_account
        else:
            self.target = self.target_id
        print('----------FB-----------')
        print(self.__dict__)
        print('==========FB===========')

    def get_page_content_by_request(self):
        if self.page_type == 'profile':
            return self.get_page_content_profile()
        if self.page_type == 'message':
            return self.get_page_content_message()
        if self.page_type == 'friend':
            return self.get_page_content_friend()

    def get_page_content_message(self):
        url = message_url_pattern.format(target=self.target)
        try:
            login_status = start_selenium(url)
            if login_status:
                # 没登录的时候，page可以继续采，所以这里不退出
                print(login_status)
            scroll(self.page_count)
            time.sleep(5)
            page_source = driver.page_source
            driver.close()
            return page_source

        except Exception as e:
            print(e)
            driver.close()

    def get_page_content_profile(self):
        url = profile_url_pattern.format(target=self.target)
        try:
            login_status = start_selenium(url)
            if login_status:
                # 没登录的时候，page可以继续采，所以这里不退出
                print(login_status)
            page_source = driver.page_source
            author_id = get_author_id(page_source)
            author_account = get_author_account(page_source)
            author_name = get_author_name(page_source)
            author_profile_image = get_author_profile_image(driver)
            about = {}
            url = driver.current_url
            url = create_original_link(url)
            print("\nScraping:", url)
            print("----------------------------------------")
            # 如果是page，只返回page_about
            page_id = get_middle_str(page_source, '"pageID":"', '"')
            if page_id:
                page_url = url + "/about/"
                try:
                    driver.get(page_url)
                    time.sleep(5)
                    data = driver.find_elements_by_xpath('//*[contains(@id,"PagesProfileAboutInfoPagelet")]')
                    about["page_about"] = data[0].get_attribute('innerHTML')

                except Exception as e:
                    print(e)
            # ---------------------------------------------------------------------------------------------------------
            # user获取的profile
            if not page_id:
                scan_list = ["education", "living", "overview", "bio", "contact_info", "relationship", "year_overviews"]
                section = ["/about?section=education", "/about?section=living", "/about?section=overview",
                           "/about?section=bio", "/about?section=contact-info", "/about?section=relationship",
                           "/about?section=year-overviews"]
                # =====WSC: modify xpath=========
                elements_path = ["//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul/li/div/div[2]/div/div"] * 7
                page = []
                for i in range(len(section)):
                    page.append(url + section[i])

                for i in range(len(page)):
                    try:
                        driver.get(page[i])
                        time.sleep(5)
                        data = driver.find_elements_by_xpath(elements_path[i])
                        about[scan_list[i]] = data[0].get_attribute('innerHTML')

                    except Exception as e:
                        print(e)

            driver.close()
            about_result = {"author_id": author_id, "author_account": author_account, "author_name": author_name,
                            "author_profile_image": author_profile_image, "about": about}
            result = json.dumps(about_result, ensure_ascii=False)
            # 再进行html编码，这样最终flask输出才是合法的json
            html_result = html.escape(result)
            print("About Section Done")
            return html_result

        except Exception as e:
            print(e)
            driver.close()

    def get_page_content_friend(self):
        url = friend_url_pattern.format(target=self.target)
        try:
            login_status = start_selenium(url)
            if login_status:
                # 没登录的时候，friend没法采集，这里直接退出
                print(login_status)
                friend_result = {"author_id": "", "friend_list": {}, "status_message": "Not Login!"}
                result = json.dumps(friend_result, ensure_ascii=False)
                driver.close()
                return result

            page_source = driver.page_source
            author_id = get_author_id(page_source)
            # 如果是page，就返回空
            page_id = get_middle_str(page_source, '"pageID":"', '"')
            if page_id:
                friend_result = {"author_id": author_id, "friend_list": {}, "status_message": "It's Page. No friends."}
                result = json.dumps(friend_result, ensure_ascii=False)
                driver.close()
                return result

            url = driver.current_url
            url = create_original_link(url)
            print("\nScraping:", url)
            print("----------------------------------------")
            print("Friends..")
            # 暂时只获取前面三个，避免封号
            # scan_list = ["All", "Following", "Followers", "Work", "College", "Current City", "Hometown"]
            # section = ["/friends", "/following", "/followers", "/friends_work", "/friends_college",
            #            "/friends_current_city", "/friends_hometown"]
            scan_list = ["All", "Following", "Followers"]
            section = ["/friends", "/following", "/followers"]
            # =====WSC: modify xpath=========
            elements_path = ["//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li",
                             "//*[@id='pagelet_collections_following']/ul/li",
                             "//*[contains(@class,'fbProfileBrowserListItem')]/div/a",
                             "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li",
                             "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li",
                             "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li",
                             "//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li"]
            # 结果键不要出现空格，采集软件不支持，Current City-->CurrentCity
            friend_list = {"All": [], "Following": [], "Followers": [], "Work": [], "College": [], "CurrentCity": [],
                           "Hometown": []}
            no_friends_to_show = 0

            page = []
            for i in range(len(section)):
                page.append(url + section[i])

            for i in range(len(page)):
                try:
                    driver.get(page[i])
                    time.sleep(10)
                    # 获取朋友栏目名，如果节点不存在，说明是no_friends_to_show,退出循环
                    try:
                        sections_bar = driver.find_element_by_xpath("//*[@class='_3cz'][1]/div[2]/div[1]")
                    except Exception as e:
                        no_friends_to_show = 1
                        break

                    # 如果有栏目，但是当前栏目如follower不存在，则继续下一个栏目采集
                    if sections_bar.text.find(scan_list[i]) == -1:
                        continue
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # 暂时不要翻页，防止封号
                    # scroll(self.page_count)
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    data = driver.find_elements_by_xpath(elements_path[i])
                    results = [x for x in data]

                    for j in range(len(results)):
                        # friend_author_id
                        friend_author_id_element = results[j].find_element_by_xpath(
                            ".//a[contains(@data-hovercard,'/ajax/hovercard/user.php?id=') and contains(@data-gt,'engagement')]")
                        friend_author_id = \
                            friend_author_id_element.get_attribute("data-hovercard").split("user.php?id=")[1].split(
                                "&")[0]
                        # friend_author_name
                        friend_author_name_element = results[j].find_element_by_xpath(
                            ".//a[contains(@data-hovercard,'/ajax/hovercard/user.php?id=') and contains(@data-gt,'engagement')]")
                        friend_author_name = friend_author_name_element.text
                        # friend_author_url
                        friend_author_url_element = results[j].find_element_by_xpath("./div/a")
                        friend_author_url = friend_author_url_element.get_attribute("href")
                        friend_author_url = friend_author_url.replace(
                            "&fref=profile_friend_list&hc_location=friends_tab",
                            "")
                        friend_author_url = friend_author_url.replace(
                            "?fref=profile_friend_list&hc_location=friends_tab",
                            "")
                        # img_url
                        friend_img_url_element = results[j].find_element_by_xpath("./div/a/img")
                        friend_img_url = friend_img_url_element.get_attribute("src")

                        item = {"author_id": friend_author_id, "author_name": friend_author_name,
                                "author_url": friend_author_url, "img_url": friend_img_url}
                        # 结果键不要出现空格，采集软件不支持，Current City-->CurrentCity
                        friend_result_key = scan_list[i].replace(' ', '')
                        friend_list[friend_result_key].append(item)

                except Exception as e:
                    print(e)

            driver.close()
            if no_friends_to_show:
                friend_result = {"author_id": author_id, "friend_list": friend_list,
                                 "status_message": "no friends to show"}
            else:
                friend_result = {"author_id": author_id, "friend_list": friend_list,
                                 "status_message": "success"}
            result = json.dumps(friend_result, ensure_ascii=False)
            # print(result)
            print("Friends Done")
            return result

        except Exception as e:
            print(e)
            driver.close()


# =============================================================================

def main():

    params = {
        'page_type': 'message',
        'target_account': 'DonaldTrump',
    }
    result = FacebookAgent(params).get_page_content_by_request()
    print(result)


if __name__ == '__main__':
    main()
