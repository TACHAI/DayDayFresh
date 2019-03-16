# 使用celery
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail


# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks',broker='redis://')

# 定义任务函数
@app.task
def send_register_active_email(to_email,username,token):
    '''发送激活邮件'''

    subject = 'django学习'
    message = '邮件正文 欢迎注册'
    sender = settings.EMAIL_FROM

    html_message = ''
    # 收件人列表
    receiver = [to_email]
    send_mail(subject, message, sender, receiver, html_message)
