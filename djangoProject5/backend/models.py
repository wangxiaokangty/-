
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from backend.universalFunctions.encrypt import encrypt_data, decrypt_data


# Create your models here.
class User(models.Model):
    user_type_choice=[('normalUser','normalUser'),('admin','admin')]
    user_id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    username= models.CharField(default='username', max_length=50,unique=True)
    password= models.TextField()
    email= models.CharField(default='email', max_length=350)
    userBalance= models.FloatField(default=0.0)
    userCreditRank= models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    userType= models.CharField(default='normalUser', max_length=20, choices=user_type_choice)
    userCurrentExp= models.IntegerField(default=0)
    #定义加密函数，加密密码属性
    def set_encrpted_password(self, password):
        self.password = encrypt_data(password)
    def get_decrpted_password(self):
        return decrypt_data(self.password)


class Task(models.Model):
    #定义类型的数据域
    question_type_choices=[('单选题','单选题'),('多选题','多选题'),('填空题','填空题'),('框图题','框图题')]
    data_type_choices=[('文本','文本'),('图片','图片')]
    task_status_choices=[('审核未通过','审核未通过'),('审核中','审核中'),('进行中','进行中'),('提前终止','提前终止'),('已逾期','已逾期')]
    #声明各个字段
    task_id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    task_name = models.CharField(default='', max_length=50)
    task_description = models.CharField(default='', max_length=500)
    data_type = models.CharField(default='image', max_length=20, choices=data_type_choices)
    data_nums = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    task_rank = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    each_pay= models.FloatField(default=0.0)
    question_description = models.CharField(default='', max_length=500)
    question_type = models.CharField(default='单选题', max_length=20, choices=question_type_choices)
    options = models.JSONField(default=dict)
    publisher= models.ForeignKey(User, to_field="username",on_delete=models.CASCADE)
    task_status=models.CharField(default='审核中', max_length=20, choices=task_status_choices)
    release_time=models.DateTimeField(default=timezone.now)
    #默认一周后截止
    deadline_time=models.DateTimeField(default=timezone.now)

class SubTask(models.Model):
    subtask_status_choices=[('未领取','未领取'),('未完成','未完成'),('已完成','已完成'),('举报中','举报中'),('举报已解决','举报已解决')]

    subtask_id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    task= models.ForeignKey(Task, on_delete=models.CASCADE)
    subtask_index = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    content= models.CharField(default='', max_length=500)
    receiver = models.ForeignKey(User, to_field="username",on_delete=models.CASCADE, null=True, blank=True)
    answer = models.CharField(default='', max_length=500)
    finish_time=models.DateTimeField(null=True, blank=True)
    subtask_status=models.CharField(default='未领取', max_length=20, choices=subtask_status_choices)
class Message(models.Model):
    id= models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    time= models.DateTimeField(default=timezone.now)
    sender= models.CharField(default='', max_length=50)
    receiver= models.ForeignKey(User, to_field="username",on_delete=models.CASCADE, related_name='receiver')
    task= models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task')
    subtask= models.ForeignKey(SubTask, on_delete=models.CASCADE, related_name='subtask',null=True, blank=True)
    content= models.CharField(default='', max_length=500)