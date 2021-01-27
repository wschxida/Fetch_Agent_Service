
import html
import json
import os


curpath = os.path.dirname(os.path.realpath(__file__))


def extractor_get_profile(username, html_code='0'):
    target_profile = []
    status = '0'
    error = None

    try:
        cmd = f'''python3 {curpath}/os_system_run.py get_profile {username}'''
        os.system(cmd)

        # 读取结果，返回
        file_name = os.path.join(curpath, "author", username.lower() + "_profile.json")
        fl = open(file_name, 'r', encoding='utf-8')
        file_read = fl.read()
        if len(file_read) > 0:
            status = '1'
        target_profile = json.loads(file_read)

    except Exception as e:
        error = str(e)
        print(e)

    result = {"status": status, "error": error, "agent_type": "telegram", "fetch_type": "get_profile",
              "target_profile": target_profile, "data_item_count": 1, "data": ''}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
    if html_code == '1':
        return html_result
    else:
        return json_result


def main():
    # username = 'drafts4'    # group
    # username = 'aboutipad'  # group
    username = 'tieliu'  # channel
    # username = '1306732370'
    result = extractor_get_profile(username)
    print(result)


if __name__ == '__main__':
    main()
