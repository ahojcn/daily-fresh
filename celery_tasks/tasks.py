# 使用 celery
from celery import Celery
from django.core.mail import send_mail
from django.conf import settings

# 在任务处理者加下面 4 句
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
django.setup()

# 创建 celery 的实例对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')  # 10.211.55.6:6379/8


# 定义人物函数
@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    # 发邮件
    htmlmsg = '<h1>欢迎，%s<h1><br>请点击下面的链接激活您的账户：<br>' \
              '<a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' \
              % (username, token, token)
    send_mail("标题", "", settings.EMAIL_FROM, recipient_list=[to_email], html_message=htmlmsg)
