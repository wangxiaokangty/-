import json
import os

from django.http import HttpResponse
from django.shortcuts import render
import time

from django.views.decorators.csrf import csrf_exempt

from backend.dataBaseOperations.create import *
from backend.dataBaseOperations.delete import *
from backend.dataBaseOperations.search import *
from backend.dataBaseOperations.update import *
from backend.globalVariables.Constraints import TASK_MATERIAL_SAVE_PATH
from backend.universalFunctions.functions import *
#注册函数
def log_up(request):
    query_dict = request.GET
    type = query_dict.get("type", "")
    email = query_dict.get("email", "")
    username = query_dict.get("username", "")

    # 如果是发邮箱,verifyCode返回应该的验证码
    if type == 'getVerifyCode':
        is_user_exist = is_exist_user_email(email)
        if is_user_exist:
            return HttpResponse(json.dumps({'status': 'error', 'message': 'sameEmail'}), content_type='application/json')
        code = send_email(email)
        return HttpResponse(json.dumps({'status': 'ok', 'verifyCode': code}), content_type='application/json')

    # 如果是点击注册
    elif type == 'logUp':
        basic_user_info={}
        # 判断是否重名
        is_user_exist = is_exist_user_name(username)
        if is_user_exist:
            return HttpResponse(json.dumps({'status': 'error', 'message': 'sameName'}), content_type='application/json')
        basic_user_info["username"] = username
        basic_user_info["email"] = email
        basic_user_info["password"] = query_dict.get("password", "")
        basic_user_info["userType"]= query_dict.get("userType", "normalType")
        basic_user_info["userCreditRank"] = query_dict.get("userCreditRank", 1)
        basic_user_info["userCurrentExp"] = query_dict.get("userCurrentExp", 0)
        basic_user_info["userBalance"] = query_dict.get("userBalance", 0.0)
        if create_a_user(**basic_user_info):
            return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'error', 'message': 'unknown'}), content_type='application/json')

    # 未知操作
    else:
        return HttpResponse(json.dumps({'status': 'error', 'message': 'unknownOperation'}),
                            content_type='application/json')

#登录函数
def log_in(request):
    query_dict = request.GET
    username = query_dict.get("username", "")
    password = query_dict.get("password", "")
    user= get_user_by_name(username)

    if not is_exist_user_name(username):
        return HttpResponse(json.dumps({'status': 'error', 'message': 'noUser'}), content_type='application/json')
    # 查看是否是管理员
    if user.userType == 'admin':
        if password == user.get_decrpted_password():
            return HttpResponse(json.dumps({'status': 'ok', 'message': '管理员登录成功','type':'admin'}))
        else:
            return HttpResponse(json.dumps({'status': 'error', 'message': 'wrongPassword'}))
    # 普通用户
    else:
        if password == user.get_decrpted_password():
            return HttpResponse(json.dumps({'status': 'ok', 'message': '登录成功','type':'normal'}))
        else:
            return HttpResponse(json.dumps({'status': 'error', 'message': 'wrongPassword'}))

# 发送验证码
def send_verify_code(request):
    email = request.GET.get('email')
    username = request.GET.get('username')
    # 验证用户名是否存在
    if not is_exist_user_name(username):
        return HttpResponse(json.dumps({'status': 'error', 'message': '当前用户名不存在'}), content_type='application/json')
    # 验证邮箱是否存在
    user = User.objects.filter(email=email, username=username).first()
    if not user:
        return HttpResponse(json.dumps({'status': 'error', 'message': '邮箱错误'}), content_type='application/json')
    # 生成验证码
    code = send_email(email)
    return HttpResponse(json.dumps({'status': 'ok', 'verifyCode': code}), content_type='application/json')

# 重置密码
@csrf_exempt
def reset_password(request):
    data = request.POST
    username = data.get('username')
    email = data.get('email')
    new_password = data.get('newPassword')
    User.objects.filter(username=username, email=email).update(password=new_password)
    return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')


#获取用户信息
def get_user(request):
    query_dict = request.GET
    params_dict = {}
    for key in query_dict:
        params_dict[key] = query_dict[key]
    user_info = get_user_info(**params_dict)
    if not user_info:
        return HttpResponse(json.dumps({'status': 'error', 'message': '无满足条件的用户'}), content_type='application/json')
    return HttpResponse(json.dumps({"status":"ok","data":user_info}), content_type='application/json')

#更新用户信息
def update_userInfo(request):
    query_dict = request.GET
    params_json = query_dict.get("params", "")
    params = json.loads(params_json)
    if 'username' not in params:
        return HttpResponse(json.dumps({'status': 'wrong', 'type': 'noUserName'}), content_type='application/json')
    else:
        username = params['username']
        if not is_exist_user_name(username):
            return HttpResponse(json.dumps({'status': 'wrong', 'type': 'noUser'}), content_type='application/json')
        if update_user_info(**params):
            return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'wrong', 'type': 'unknown'}), content_type='application/json')

def top_up(request):
    query_dict = request.GET
    username = query_dict.get("username", "")
    amount = float(query_dict.get("balance_change", 0))
    if not is_exist_user_name(username):
        return HttpResponse(json.dumps({'status': 'error', 'message': '用户不存在'}), content_type='application/json')
    if amount<0:
        return HttpResponse(json.dumps({'status': 'error', 'message': '金额错误'}), content_type='application/json')
    if update_user_balance(username, amount):
        return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': 'error', 'message': '未知错误'}), content_type='application/json')

@csrf_exempt
def post_task(request):
    if request.method=="POST" and request.FILES.get("file",None):
        task_basic_info={}
        query_dict= request.POST
        task_basic_info["task_name"]=query_dict.get("task_name","")
        if is_exist_task_name(task_basic_info["task_name"]):
            return HttpResponse(json.dumps({'status': 'error', 'message': '任务名重复'}), content_type='application/json')
        task_basic_info["task_description"]=query_dict.get("task_description","")
        task_basic_info["data_type"]=query_dict.get("data_type","")
        task_basic_info["task_rank"]=query_dict.get("task_rank","")
        task_basic_info["each_pay"]=query_dict.get("each_pay","")
        task_basic_info["question_description"]=query_dict.get("question_description","")
        task_basic_info["options"]=query_dict.get("options","")
        task_basic_info["question_type"] = query_dict.get("question_type", "")
        task_basic_info["release_time"] = timezone.now()
        #djang的规范，当外键不是其他表的主键时，这个外键的实际传入是被参考对象的实例
        publisher = query_dict.get("publisher", "")
        task_basic_info["publisher"] = get_user_by_name(username=publisher)
        #默认截止日期为一周后
        if not query_dict.get("deadline_time",None):
            task_basic_info["deadline_time"] = timezone.now()+datetime.timedelta(days=7)
        else:
            task_basic_info["deadline_time"] = query_dict.get("deadline_time", "")
        user_info = get_user_by_name(username=publisher)
        if (user_info.userBalance < 0):
            return HttpResponse(json.dumps({'status': 'error', 'message': f'当前用户余额已低于0，请充值后再发布任务！当前余额: {user_info.userBalance}'}), content_type='application/json')
        
        file = request.FILES["file"]
        file_path=TASK_MATERIAL_SAVE_PATH+task_basic_info["task_name"]+task_basic_info["release_time"].strftime("%Y_%m_%d_%H_%M_%S")+"/"
        #文件的处理
        if task_basic_info["data_type"]=="图片":
            if is_image_zip(file):
                file.seek(0)
                if not unzip_file(file,file_path):
                    return HttpResponse(json.dumps({'status': 'error', 'message': 'zip文件未能成功解压'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status': 'error', 'message': 'zip文件只能包含图片'}), content_type='application/json')

        elif task_basic_info["data_type"]=="文本":
            if not save_csv(file,file_path):
                return HttpResponse(json.dumps({'status': 'error', 'message': 'csv文件保存失败'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'error', 'message': '数据类型错误'}), content_type='application/json')
        #创建任务(django数据模型操作很令人费解，当外键并不关联id字段时，在创建时需要传入一个实体)
        if not create_a_task(**task_basic_info):
            return HttpResponse(json.dumps({'status': 'error', 'message': '任务创建失败'}), content_type='application/json')

        task_id = get_task_id(**task_basic_info)

        sub_tasks_info=get_sub_task_info(task_id, file_path,task_basic_info["data_type"])
        for sub_task_info in sub_tasks_info:
            if not create_a_subtask(**sub_task_info):
                return HttpResponse(json.dumps({'status': 'error', 'message': '子任务创建失败'}), content_type='application/json')

        #更新任务个数
        data_nums=len(sub_tasks_info)
        update_task_info(task_id=task_id,data_nums=data_nums)
        #扣除发布者的余额
        cost=float(task_basic_info["each_pay"])*data_nums
        status=update_user_balance(username=query_dict.get("publisher",""),balance_change=-cost)
        if status=='余额修改成功':
            return HttpResponse(json.dumps({'status': 'ok','message':f"成功创建任务！共包含{data_nums}条数据，已预先支付{cost}元！"}), content_type='application/json')
        elif status=='余额不足':
            user_balance=get_user_balance(username=query_dict.get("publisher",""))
            return HttpResponse(json.dumps({'status': 'ok', 'message':f"成功创建任务！共包含{data_nums}条数据，已预先支付{cost}元！"
                                                                         f"[请注意，扣除后余额不足，余额{user_balance}]"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'error', 'message': '更新余额失败'}), content_type='application/json')

    elif request.method=="POST" and not request.FILES.get("file",None):
        return HttpResponse(json.dumps({'status': 'error', 'message': '未上传任何文件'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': 'error', 'message': '非post请求'}), content_type='application/json')


def get_tasks(request):
    query_dict = request.GET
    params_dict = {}
    for key in query_dict:
        params_dict[key] = query_dict[key]
    if params_dict:
        params = params_dict
    else:
        params={}
    if "receiver" not in params.keys() and "subtask_status" not in params.keys():
        task_dicts = get_task_info(**params)
        if not task_dicts:
            return HttpResponse(json.dumps({'status': 'error', 'message': '无满足条件任务'}), content_type='application/json')
        return HttpResponse(json.dumps({"status":"ok","data":task_dicts}), content_type='application/json')
    elif "receiver" in params.keys():
        receiver=get_user_by_name(params["receiver"])
        subtask_dicts=get_subtask_info(receiver=receiver)
        task_ids=[]
        for subtask_dict in subtask_dicts:
            task_id=subtask_dict["task"]
            if task_id not in task_ids:
                task_ids.append(task_id)
        task_dicts=[]
        for task_id in task_ids:
            task_dict=get_task_info(task_id=task_id)[0]
            task_dicts.append(task_dict)
        if not task_dicts:
            return HttpResponse(json.dumps({'status': 'error', 'message': '无满足条件任务'}), content_type='application/json')
        return HttpResponse(json.dumps({"status":"ok","data":task_dicts}), content_type='application/json')
    elif "subtask_status" in params.keys():
        subtask_dicts=get_subtask_info(subtask_status=params["subtask_status"])
        task_ids=[]
        for subtask_dict in subtask_dicts:
            task_id=subtask_dict["task"]
            if task_id not in task_ids:
                task_ids.append(task_id)
        task_dicts=[]
        for task_id in task_ids:
            task_dict=get_task_info(task_id=task_id)[0]
            task_dicts.append(task_dict)
        if not task_dicts:
            return HttpResponse(json.dumps({'status': 'error', 'message': '无满足条件任务'}), content_type='application/json')
        return HttpResponse(json.dumps({"status":"ok","data":task_dicts}), content_type='application/json')

def get_subtasks(request):
    query_dict = request.GET
    params_dict = {}
    for key in query_dict:
        params_dict[key] = query_dict[key]
    if params_dict:
        params = params_dict
    else:
        params = {}
    subtask_dicts=get_subtask_info(**params)
    if not subtask_dicts:
        return HttpResponse(json.dumps({"status":"error",'message':"无满足条件子任务"}),content_type='application/json')
    
    # 定义状态的排序优先级
    status_priority = {
        "未完成": 1,
        "已完成": 2,
        "未领取": 3,
        "举报中": 4,
        "举报已解决":5
    }
    # 对子任务进行排序
    subtask_dicts.sort(key=lambda x: status_priority[x['subtask_status']])
    return HttpResponse(json.dumps({'status':"ok",'data':subtask_dicts}),content_type='application/json')



@csrf_exempt
def admin_submit_review(request):
    query_dict= request.POST
    task_id=query_dict.get("task_id","")
    approval_status=query_dict.get("approvalStatus","")
    rejection_reason=query_dict.get("rejectionReason","")
    if not is_exist_task_id(task_id):
        return HttpResponse(json.dumps({'status': 'error', 'message': '任务不存在'}), content_type='application/json')
    if approval_status!="false":
        data={"task_id":task_id,"task_status":"进行中"}
        update_task_info(**data)
        return HttpResponse(json.dumps({'status': 'ok', 'message': '审核结果提交成功'}), content_type='application/json')
    else:
        data={"task_id":task_id,"task_status":"审核未通过"}
        cost=get_task_info(task_id=task_id)[0]["each_pay"]*get_task_info(task_id=task_id)[0]["data_nums"]
        username=get_task_info(task_id=task_id)[0]["publisher"]
        publisher=get_user_by_name(username)
        update_user_balance(username=username,balance_change=cost)
        message={"time":timezone.now(),"task_id":task_id,"sender":"管理员",
                 "receiver":publisher,"content":f"你的任务{task_id}审核未通过，原因：{rejection_reason},任务报酬{cost}元已退回"}
        update_task_info(**data)
        if not create_a_message(**message):
            return HttpResponse(json.dumps({'status': 'error', 'message': '消息创建失败'}), content_type='application/json')
        return HttpResponse(json.dumps({'status': 'ok', 'message': '审核结果提交成功'}), content_type='application/json')

def get_messages(request):
    query_dict=request.GET
    params_dict={}
    for key in query_dict:
        params_dict[key] = query_dict[key]
    messages=get_message_by_receiver(params_dict["username"])
    if not messages:
        return HttpResponse(json.dumps({'status': 'error', 'message': 'No data'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': 'ok', 'data': messages}), content_type='application/json')

@csrf_exempt
def terminate_task(request):
    query_dict=request.POST
    task_id=query_dict.get("task_id","")
    if not is_exist_task_id(task_id):
        return HttpResponse(json.dumps({'status': 'error', 'message': '任务不存在'}), content_type='application/json')
    type=query_dict.get("type","")
    # 返回发布者金额
    publisher = get_task_publisher(task_id)
    unfinished_num = get_unfinished_num(task_id)
    each_pay = get_task_each_pay(task_id)
    refund = unfinished_num * each_pay
    # 更新发布者余额
    update_user_balance(publisher.username, refund)
    update_task_info(task_id=task_id, task_status=type)
    if type == "已逾期":
        message_to_publisher = {
            "time": timezone.now(),
            "sender": "系统自动发送",
            "receiver": publisher,
            "task_id": task_id,
            "content": f"任务逾期,{unfinished_num}条数据未标注，返回{refund}元报酬"
        }
        if not create_a_message(**message_to_publisher):
            return HttpResponse(json.dumps({"status": "error", "message": "发送给任务发布者的消息失败"}))
        #扣除未完成用户的经验值
        unfinished_user_subtasks=get_task_unfinished_user_subtasks(task_id)
        for user_subtask in unfinished_user_subtasks:
            update_user_exp(user_subtask[0].username,-20)
            update_user_credit_rank(user_subtask[0].username)
            message_to_receiver={
                "time":timezone.now(),
                "sender":"系统自动发送",
                "receiver":user_subtask[0],
                "task_id":task_id,
                "subtask_id":user_subtask[1],
                "content":f"任务逾期未完成，扣除20点经验"
            }
            if not create_a_message(**message_to_receiver):
                return HttpResponse(json.dumps({"status":"error","message":"发送给任务接收者的消息失败"}),content_type='application/json')
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')
    elif type=="提前终止":
        return HttpResponse(json.dumps({"status": "ok","message":f"成功提前终止任务！[当前{unfinished_num}"
                                                                 f"条数据未处理，返回金额：{refund}元]"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"status": "error", "message": "终止状态错误"}), content_type='application/json')

@csrf_exempt
def update_subtask_receiver(request):
    query_dict=request.POST
    task_id=query_dict.get("task_id","")
    receiver = get_user_by_name(query_dict.get("receiver", ""))
    if not task_id or not receiver:
        return HttpResponse(json.dumps({"status":"error","message":"任务或领取者不存在"}), content_type='application/json')
    #发布者不可领取自己的任务
    if not check_not_publisher_receive(task_id,receiver):
        return HttpResponse(json.dumps({"status":"error","message":"发布者不可领取任务"}), content_type='application/json')
    #未审核任务不可领取
    if get_task_info(task_id=task_id)[0]["task_status"]!="进行中":
        return HttpResponse(json.dumps({"status":"error","message":"任务不在进行中,不可领取"}), content_type='application/json')
    #领取者星级不足不可领取
    if receiver.userCreditRank<get_task_info(task_id=task_id)[0]["task_rank"]:
        return HttpResponse(json.dumps({"status":"error","message":"领取者星级不足"}), content_type='application/json')
    subtask_index=int(query_dict.get("subtask_index",""))
    subtask_id=get_subtask_id_by_index(task_id,subtask_index)
    if not subtask_id:
        return HttpResponse(json.dumps({"status":"error","message":"不存在子任务"}), content_type='application/json')
    receiver=get_user_by_name(query_dict.get("receiver",""))
    data={"subtask_id":subtask_id,"receiver":receiver,"subtask_status":"未完成"}
    update_subtask_info(**data)
    if not update_subtask_info(**data):
        return HttpResponse(json.dumps({"status":"error","message":"更新子任务失败"}), content_type='application/json')
    return HttpResponse(json.dumps({"status":"ok"}), content_type='application/json')

# done
@csrf_exempt
def submit_subtask_answer(request):
    query_dict=request.POST
    print(query_dict)
    task_id=query_dict.get("task_id","")
    subtask_index=int(query_dict.get("subtask_index",""))
    answer=query_dict.get("answer","")
    subtask_id=get_subtask_id_by_index(task_id,subtask_index)
    if not subtask_id:
        return HttpResponse(json.dumps({"status":"error","message":"不存在子任务"}), content_type='application/json')
    subtask_status=get_subtask_info(subtask_id=subtask_id)[0]["subtask_status"]
    if subtask_status!="未完成":
        return HttpResponse(json.dumps({"status":"error","message":"子任务不在待完成状态"}), content_type='application/json')
    data={"subtask_id":subtask_id,"answer":answer,"subtask_status":"已完成","finish_time":timezone.now()}
    if not update_subtask_info(**data):
        return HttpResponse(json.dumps({"status":"error","message":"更新子任务失败"}), content_type='application/json')
    receiver=get_subtask_receiver(subtask_id)
    #更新信息
    update_user_exp(receiver.username,10)
    update_user_credit_rank(receiver.username)
    each_pay=get_task_each_pay(task_id)
    update_user_balance(receiver.username,each_pay)
    return HttpResponse(json.dumps({"status":"ok"}), content_type='application/json')

@csrf_exempt
def report_subtask(request):
    query_dict=request.POST
    task_id=query_dict.get("task_id","")
    #很奇怪，同样传过来数字，task_id不需要类型转化，这可能是由于task_id是主键而subtask_index只是普通字段
    subtask_index=int(query_dict.get("subtask_index",""))
    subtask_id=get_subtask_id_by_index(task_id,subtask_index)
    if get_subtask_info(subtask_id=subtask_id)[0]["subtask_status"] !="已完成":
        if get_subtask_info(subtask_id=subtask_id)[0]["subtask_status"] =="举报中":
            return HttpResponse(json.dumps({"status":"error","message":"子任务正在举报中"}), content_type='application/json')
        elif get_subtask_info(subtask_id=subtask_id)[0]["subtask_status"] =="举报已解决":
            return HttpResponse(json.dumps({"status":"error","message":"举报已解决，不可再次举报"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status":"error","message":"子任务不是完成状态，不可举报"}), content_type='application/json')
    data={"subtask_id":subtask_id,"subtask_status":"举报中"}
    if not update_subtask_info(**data):
        return HttpResponse(json.dumps({"status":"error","message":"更新子任务失败"}), content_type='application/json')
    return HttpResponse(json.dumps({"status":"ok","message":"举报提交成功，等待管理员评估后反馈信息"}), content_type='application/json')

@csrf_exempt
def process_report(request):
    query_dict=request.POST
    task_id=query_dict.get("task_id","")
    subtask_index=int(query_dict.get("subtask_index",""))
    approval_status=query_dict.get("approvalStatus","")
    subtask_id=get_subtask_id_by_index(task_id,subtask_index)
    if get_subtask_info(subtask_id=subtask_id)[0]["subtask_status"]!="举报中":
        return HttpResponse(json.dumps({"status":"error","message":"子任务不在举报中状态"}), content_type='application/json')
    data = {"subtask_id": subtask_id, "subtask_status": "举报已解决"}
    if not update_subtask_info(**data):
        return HttpResponse(json.dumps({"status": "error", "message": "更新子任务失败"}),
                            content_type='application/json')
    if approval_status!="false":
        #惩罚领取者
        each_pay=get_task_each_pay(task_id)
        receiver=get_subtask_receiver(subtask_id)
        update_user_balance(receiver.username,-each_pay)
        update_user_exp(receiver.username,-10)
        update_user_credit_rank(receiver.username)
        message_to_receiver={
            "time":timezone.now(),
            "sender":"管理员",
            "receiver":receiver,
            "task_id":task_id,
            "subtask_id":subtask_id,
            "content":f"经审核，该数据数据标注质量不过关，扣除10点经验和对应报酬"
        }
        if not create_a_message(**message_to_receiver):
            return HttpResponse(json.dumps({"status":"error","message":"发送给任务接收者的消息失败"}),content_type='application/json')
        #返回发布者金额
        publisher=get_task_publisher(task_id)
        update_user_balance(publisher.username,each_pay)
        message_to_publisher={
            "time":timezone.now(),
            "sender":"管理员",
            "receiver":publisher,
            "task_id":task_id,
            "subtask_id":subtask_id,
            "content":f"经审核，你的举报属实，已返回对应报酬"
        }
        if not create_a_message(**message_to_publisher):
            return HttpResponse(json.dumps({"status":"error","message":"发送给任务发布者的消息失败"}),content_type='application/json')
    else:
        publisher=get_task_publisher(task_id)
        message_to_publisher={
            "time":timezone.now(),
            "sender":"管理员",
            "receiver":publisher,
            "task_id":task_id,
            "subtask_id":subtask_id,
            "content":f"经审核，标注数据质量合格，举报无效"
        }
        if not create_a_message(**message_to_publisher):
            return HttpResponse(json.dumps({"status":"error","message":"发送给任务发布者的消息失败"}),content_type='application/json')
    return HttpResponse(json.dumps({"status":"ok","message":"举报处理成功"}),content_type='application/json')

