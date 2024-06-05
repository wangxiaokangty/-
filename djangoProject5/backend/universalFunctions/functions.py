import csv
import datetime
import glob
import json
import os
import random
import zipfile
from io import BytesIO

from PIL.Image import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.http import HttpResponse

from backend.globalVariables.Constraints import TEMP_ZIP_FILE_PATH, TASK_MATERIAL_SAVE_PATH



#定义发送邮件的函数
def send_email(email):
    #定义邮件标题
    subject = '验证码'
    code=''
    for i in range(6):
        code += str(random.randint(0, 9))
    #定义邮件内容
    message = '您的验证码为：' + code
    #定义发送者
    recipient_list=[email]
    from_email = "18954600862@163.com"
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return code

#检查是否是图片格式，可以为jpg,png,jpeg
def is_image(file_bytes):
    jpeg_start = b'\xff\xd8'
    # PNG 文件以 89 50 4E 47 0D 0A 1A 0A 开头
    png_signature = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    if file_bytes.startswith(jpeg_start):
        return True
    if file_bytes.startswith(png_signature):
        return True
    return False
#检查zip文件是否满足上述格式
def is_image_zip(file):
    try:
        files_bytes = file.read()
        with zipfile.ZipFile(BytesIO(files_bytes), 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if not file_info.is_dir():
                    with zip_ref.open(file_info) as file:
                        file_bytes = file.read()
                        if not is_image(file_bytes):
                            return False

    except Exception:
        return False
    return True



#解压缩zip文件
def unzip_file(file,file_path):
    #判断是否存在文件夹，否则创建之
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        temp_zip_path = default_storage.save(TEMP_ZIP_FILE_PATH + file.name, ContentFile(file.read()))
        # 解压zip文件
        with zipfile.ZipFile(default_storage.path(temp_zip_path), 'r') as zip_ref:
            zip_ref.extractall(file_path)
        # 删除临时zip文件
        default_storage.delete(temp_zip_path)
        return True
    except:
        return False


#保存csv文件
def save_csv(file, file_path):
    try:
        # 保存文件
        default_storage.save(file_path + file.name, ContentFile(file.read()))
        return True
    except:
        return False


def get_sub_task_info(task_id, file_path,type):
    try:
        if type=="图片":
        # 获取指定目录中的所有图片文件
            # images = [os.path.join(file_path, f) for f in os.listdir(file_path) ]
            images = []
            # 图片文件支持的扩展名
            image_extensions = ('.jpg', '.jpeg', '.png')

            # 使用os.walk遍历file_path下的所有文件和文件夹
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    # 检查文件扩展名是否为图片格式
                    if file.lower().endswith(image_extensions):
                        # 将图片文件的完整路径添加到images列表中
                        images.append(os.path.join(root, file))
            # 按照文件名排序
            images.sort()
            # 创建子任务列表
            sub_tasks = []
            for index, image in enumerate(images):
                # TODO: 这里的路径需要修改为相对路径 如果后续有删除图片的操作，记得路径也要修改
                new_image = image.replace("./media/","http://127.0.0.1:8000/media/")
                sub_task_info = {
                    'task_id': task_id,
                    'subtask_index': index,
                    'content': new_image,
                    'subtask_status': "未领取"
                }
                sub_tasks.append(sub_task_info)
            return sub_tasks
        elif type=="文本":
            # 读取csv文件
            files = os.listdir(file_path)
            # 找到CSV文件
            csv_files = file_path+ files[0]
            with open(csv_files, mode='r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                lines = list(csv_reader)
       
            # print(lines)
            sub_tasks = []
            for index, line in enumerate(lines):
                line_str = ','.join(line)
                sub_task_info = {
                    'task_id': task_id,
                    'subtask_index': index,
                    'content':line_str,
                    'subtask_status': "未领取",
                }
                sub_tasks.append(sub_task_info)
            return sub_tasks
        else:
            return False
    except Exception as e:
        print(f"Error creating sub tasks: {e}")
        return False


