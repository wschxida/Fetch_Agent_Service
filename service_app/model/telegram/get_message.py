
import os
import html
import json


curpath = os.path.dirname(os.path.realpath(__file__))


def extractor_get_message(username, html_code='0'):
    status = '0'
    message_count = 0
    data_result = ''
    try:
        cmd = f'''python3 {curpath}/os_system_run.py get_message {username}'''
        os.system(cmd)

        # 读取结果，返回
        file_name = os.path.join(curpath, "message", username.lower() + ".json")
        fl = open(file_name, 'r', encoding='utf-8')
        file_read = fl.read()
        if len(file_read) > 0:
            status = '1'
        file_read_json = json.loads(file_read)
        data_result = file_read_json
        message_count = len(data_result)
        if 'ValueError' in data_result:
            message_count = 1

    except Exception as e:
        status = str(e)
        print(e)

    result = {"status": status, "agent_type": "telegram", "fetch_type": "get_message",
              "data_item_count": message_count, "data": data_result}
    json_result = json.dumps(result, ensure_ascii=False)
    # 再进行html编码，这样最终flask输出才是合法的json
    html_result = html.escape(json_result)
    # html_code==1是方便浏览器展示字段内容为html的，默认情况返回json格式数据
    if html_code == '1':
        return html_result
    else:
        return json_result


def main():
    username = 'drafts4'    # group
    # username = 'sgergsghetrhdgfdhgfdhf'
    # username = 'tieliu'   # channel
    # username = 'misakatech' # channel
    # username = 'PublicTestGroup'  # group
    # username = 'mogahed_1070'  # 错误的
    # username = 'aboutipad'  # group

    result = extractor_get_message(username)
    print(result)


if __name__ == '__main__':
    main()
