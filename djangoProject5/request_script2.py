import requests
import json

if __name__ == '__main__':
    url = 'http://localhost:8001/'

    #views = "admin_submit_review/"
    #params = {
    #    "task_id":19,
    #    "approvalStatus":True,
    #}

    #views = "log_up/"
    #params={
    #    "type":"logUp",
    #    "username":"wmy",
    #    "email":"19932760047@buaa.edu.com",
    #    "userBalance":0,
    #    "userCreditRank":1,
    #    "userType":"normalUser",
    #    "userCurrentExp":0,
    #    "password":"1234567"
    #}

    #views="get_messages/"
    #params={
    #    "params":json.dumps({"username":"momo"})
    #}

    views="top_up/"
    params={
        "username":"momo",
        "balance_change":10
    }
    response = requests.get(url + views, params=params)
    try:
        json_data = response.json()
        print(json_data)
    except json.JSONDecodeError as e:
        print(f" {str(e)}")
        print(response.text)
