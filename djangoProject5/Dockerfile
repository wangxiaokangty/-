# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将 requirements.txt 文件复制到工作目录
COPY requirements.txt /app/

# 可选：设置镜像源为国内
COPY pip.conf /root/.pip/pip.conf

# 安装依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 将当前目录内容复制到工作目录
COPY . /app/

# 暴露应用的端口
EXPOSE 8000

# 运行数据库迁移和启动服务器
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
