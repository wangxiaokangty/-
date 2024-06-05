import json
import requests

if __name__ == '__main__':
    url = 'http://localhost:8001/'
    #上传csv文件
    #views="post_task/"
    #file_path='C://Users//woczgl//Desktop//test.csv'
    #params = {
    #    'publisher': "momo",
    #    'task_name': "第5个任务",
    #    'task_description': "没有",
    #    'question_type': "填空题",
    #    'data_type': "文本",
    #    'question_description': "给出文本情感",
    #    'task_rank': 1,
    #    'each_pay': 0.5,
    #}
    #response = requests.post(url + views, data=params, files={"file": open(file_path, "rb")})
    #上传zip文件
    options = {'A':1,
               'B':2,
               'C':3,
               'D':4}
    options_json = json.dumps(options, ensure_ascii=False, indent=4)
    views = "post_task/"
    file_path = 'C://Users//woczgl//Desktop//data.zip'
    params = {
        'publisher': "momo",
        'task_name': "第6个任务",
        'task_description': "没有",
        'question_type': "单选题",
        'data_type': "图片",
        'question_description': "选择正确答案",
        'task_rank': 1,
        'each_pay': 0.5,
        "options":options_json,
    }
    response = requests.post(url + views, data=params, files={"file": open(file_path, "rb")})

    try:
        json_data = response.json()
        print(json_data)  # 输出解析后的 JSON 数据
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {str(e)}")
        print(response.text)

