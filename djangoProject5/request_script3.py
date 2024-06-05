# -*- coding: utf-8 -*-
import json
import requests

if __name__ == '__main__':
    url = 'http://localhost:8001/'
    #终止任务
    #views="terminate_task/"
    #params={
    #    'task_id':19,
    #    'type':"提前终止"
    #}

    #获取子任务
    #views="get_subtasks/"
    #params={"params":json.dumps({'subtask_status':"举报中",},ensure_ascii=False, indent=4)}

    #提交答案
    #views="submit_subtask_answer/"
    #params={
    #    'task_id':19,
    #    'subtask_index':1,
    #    'answer':"这是答案"
    #}

    #领取任务
    #views="update_subtask_receiver/"
    #params={"task_id":18,
    #        "subtask_index":1,
    #        "receiver":"popo"}
    #举报
    #views="report_subtask/"
    #params={
    #    "task_id":19,
    #    "subtask_index":1,
    #}

    #views="process_report/"
    #params={
    #    "task_id":19,
    #    "subtask_index":1,
    #    "approvalStatus":True
    #}

    views="get_tasks/"
    params={"params":json.dumps({"receiver":"popo"},ensure_ascii=False, indent=4)}
    response = requests.get(url + views,params=params)
    try:
        json_data = response.json()
        print(json_data)
    except json.JSONDecodeError as e:
        print(f": {str(e)}")
        print(response.text)