from django.forms import model_to_dict

from ..models import *
import math
import datetime
from backend.globalVariables.variables import *
#再次定义对象的查询操作
# 通过用户名检查用户是否存在
def is_exist_user_name(username):
    try:
        User.objects.get(username=username)
        return True
    except:
        return False

# 通过手机号检查用户是否存在
def is_exist_user_phone(mobile_number):
    try:
        User.objects.get(mobile_number=mobile_number)
        return True
    except:
        return False

# 通过邮箱检查用户是否存在
def is_exist_user_email(email):
    try:
        User.objects.get(email=email)
        return True
    except:
        return False

def get_subtask_id_by_index(task_id,index):
    try:
        subtasks=SubTask.objects.filter(task_id=task_id)
        for subtask in subtasks:
            if index==subtask.subtask_index:
                return subtask.subtask_id
        return None
    except:
        return None


def match_username_with_password(username, password):
    user = User.objects.get(username=username)

    if user.get_decrpted_password() == password:
        return True
    else:
        return False


def get_task_id(**kwargs):
    try:
        task = Task.objects.get(**kwargs)
        return task.task_id
    except:
        return None

def get_user_info(**kwargs):
    try:
        user = User.objects.get(**kwargs)
        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "userBalance": user.userBalance,
            "userCreditRank": user.userCreditRank,
            "userType": user.userType,
            "userCurrentExp": user.userCurrentExp
        }
    except:
        return None

def get_user_balance(username):
    try:
        user = User.objects.get(username=username)
        return user.userBalance
    except:
        return None

def get_user_by_name(username):
    try:
        user = User.objects.get(username=username)
        return user
    except:
        return None

def is_exist_task_name(task_name):
    try:
        Task.objects.get(task_name=task_name)
        return True
    except:
        return False

def get_task_info(**params):
    try:
        tasks = Task.objects.filter(**params)
        task_dicts=[]
        for task in tasks:
            task_dict=model_to_dict(task)
            task_dict["release_time"]=task.release_time.strftime("%Y-%m-%d %H:%M:%S")
            task_dict["deadline_time"]=task.deadline_time.strftime("%Y-%m-%d %H:%M:%S")
            task_dicts.append(task_dict)
        return task_dicts
    except:
        return None

def get_subtask_info(**params):
    try:
        subtasks = SubTask.objects.filter(**params)
        subtask_dicts=[]
        for subtask in subtasks:
            subtask_dict=model_to_dict(subtask)
            if subtask_dict["finish_time"]:
                subtask_dict["finish_time"]=subtask.finish_time.strftime("%Y-%m-%d %H:%M:%S")
            subtask_dicts.append(subtask_dict)
        return subtask_dicts
    except:
        return None



def is_exist_task_id(task_id):
    try:
        Task.objects.get(task_id=task_id)
        return True
    except:
        return False

def get_message_by_receiver(receiver):
    try:
        messages=Message.objects.filter(receiver=receiver).order_by('-time')
        message_dicts=[]
        for message in messages:
            message_dict={
                "id":message.id,
                "time":message.time.strftime("%Y-%m-%d %H:%M:%S"),
                "sender":message.sender,
                "receiver":message.receiver.username,
                "task_id":message.task_id,
                "subtask_id":message.subtask_id,
                "content":message.content
            }
            message_dicts.append(message_dict)
        return message_dicts
    except:
        return None

def get_task_unfinished_user_subtasks(task_id):
    try:
        subtasks=SubTask.objects.filter(task_id=task_id,subtask_status="未完成")
        user_subtasks=[]
        for subtask in subtasks:
            user_subtasks.append((subtask.receiver,subtask.subtask_id))
        return user_subtasks
    except:
        return None

def get_task_publisher(task_id):
    try:
        task=Task.objects.get(task_id=task_id)
        return task.publisher
    except:
        return None

def get_subtask_receiver(subtask_id):
    try:
        subtask=SubTask.objects.get(subtask_id=subtask_id)
        return subtask.receiver
    except:
        return None

def get_unfinished_num(task_id):
    try:
        subtasks=SubTask.objects.filter(task_id=task_id)
        return_n=0
        for subtask in subtasks:
            if subtask.subtask_status=="未完成" or subtask.subtask_status=="未领取":
                return_n+=1
        return return_n
    except:
        return None

def get_task_each_pay(task_id):
    try:
        task=Task.objects.get(task_id=task_id)
        return task.each_pay
    except:
        return None

def check_not_publisher_receive(task_id,receiver):
    task=Task.objects.get(task_id=task_id)
    if task.publisher.username==receiver.username:
        return False
    else:
        return True


