

import os
import html
import json


curpath = os.path.dirname(os.path.realpath(__file__))


def extractor_search_channel(username, html_code='0'):
    error = None
    status = '0'
    data_result = ''
    try:
        cmd = f'''python3 {curpath}/os_system_run.py search_channel {username}'''
        print(cmd)
        os.system(cmd)

        # 读取结果，返回
        file_name = os.path.join(curpath, "author", username.lower() + "_search.json")
        fl = open(file_name, 'r', encoding='utf-8')
        file_read = fl.read()
        if len(file_read) > 0:
            status = '1'
        data_result = json.loads(file_read)

    except Exception as e:
        status = '0'
        error = str(e)
        print(e)

    result = {"status": status, "error": error, "agent_type": "telegram", "fetch_type": "search_channel",
              "data_item_count": len(data_result), "data": data_result}
    json_result = json.dumps(result, ensure_ascii=False)
    # 为了在线显示图片
    json_result = json_result.replace('/home/kismanager/KIS/Fetch_Agent_Service/service_app',
                                      '/img')

    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
    if html_code == '1':
        return html_result
    else:
        return json_result


def main():
    search_str = 'daily'
    result = extractor_search_channel(search_str)
    # print(result)


if __name__ == '__main__':
    main()
