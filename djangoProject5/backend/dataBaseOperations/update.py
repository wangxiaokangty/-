from ..models import *
import math
import datetime

def update_user_info(**kwargs):
    try:
        if "password" in kwargs:
            user = User.objects.get(username=kwargs["username"])
            user.set_encrpted_password(kwargs["password"])
            user.save()
            return True
        User.objects.filter(username=kwargs["username"]).update(**kwargs)
        return True
    except:
        return False

def update_task_info(**kwargs):
    try:
        Task.objects.filter(task_id=kwargs["task_id"]).update(**kwargs)
        return True
    except:
        return False
def update_subtask_info(**kwargs):
    try:
        SubTask.objects.filter(subtask_id=kwargs["subtask_id"]).update(**kwargs)
        return True
    except:
        return False
def update_user_balance(username, balance_change):
    try:
        user = User.objects.get(username=username)
        user.userBalance += balance_change
        user.save()
        if balance_change<0 and user.userBalance < 0:
            return '余额不足'
        return '余额修改成功'
    except:
        print("Error updating user balance")
        return '更新失败'

def update_user_exp(username,exp_change):
    try:
        user=User.objects.get(username=username)
        user.userCurrentExp+=exp_change
        user.save()
        return True
    except:
        False

def update_user_credit_rank(username):
    try:
        experience_levels = {
            0: (-9999999, 0),
            1: (0, 100),
            2: (100, 500),
            3: (500, 1000),
            4: (1000, 2000),
            5: (2000, 99999999)
        }
        user = User.objects.get(username=username)
        exp = user.userCurrentExp
        for rank, (low, high) in experience_levels.items():
            if low <= exp < high:
                user.userCreditRank = rank
                user.save()
                return True
    except:
        return False
