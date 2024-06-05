from ..models import *
import math
import datetime

#在此定义对象的添加操作
#参数较多的直接通过字典传入，参数较少的直接传入
def create_a_user(**kwargs):
    try:
        User.objects.create(**kwargs)
        return True
    except:
        return False

def create_a_task(**kwargs):
    try:
        Task.objects.create(**kwargs)
        return True
    except Exception as e:
        print(e)
        return False

def create_a_task_test(**kwargs):
    Task.objects.create(**kwargs)


def create_a_subtask(**kwargs):
    try:
        SubTask.objects.create(**kwargs)
        return True
    except:
        return False

def create_a_message(**kwargs):
    try:
        Message.objects.create(**kwargs)
        return True
    except:
        return False
