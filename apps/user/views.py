from django.shortcuts import render,redirect
from django.core.mail import *
from django.views.generic import View
from django.http import HttpResponse
from apps.user.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from celery_tasks.tasks import send_register_active_email

import re
# Create your views here.

# /user/register
def register(request):
    '''显示注册页面'''
    if request.method == 'GET':
        return render(request,'register.html')

def register_handle(request):
    '''进行注册处理'''
    # 接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('emial')
    allow = request.POST.get('allow')
    # 进行数据校验
    if all([username,password,email]):
        # 数据不完整
        return render(request,'register.html',{'errmsg':'数据不完整'})
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request,'register.html',{'errmsg':'邮箱格式不正确'})
    if allow !='on':
        return render(request,'register.html',{'errmsg':'请同意协议'})


    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
    #     用户名不存在
        return render(request,'register.html',{'errmsg':'用户名已存在'})

    # 进行业务处理
    # user = User()
    # user.email =email
    # user.password=password
    # user.username=username
    # user.save()
    #
    # 检验用户名是否重复



    user = User.objects.create_user(username,email,password)
    user.is_active=0
    user.save()
    # 返回应答,跳转到首页 这里是写的  url中的name
    return redirect(reversed('goods:index'))


class register_view(View):

    def get(self,request):
        return render(request,'register.html')

    def post(self,request):

        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('emial')
        allow = request.POST.get('allow')
        # 进行数据校验
        if all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            #     用户名不存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 进行业务处理
        # user = User()
        # user.email =email
        # user.password=password
        # user.username=username
        # user.save()
        #
        # 检验用户名是否重复

        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 发送激活邮件，包含激活链接：
        # 激活链接中需要包含用户的身份信息，并把身份信息加密
        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY,3600)

        info ={'confirm':user.id}
        token = serializer.dumps(info)

        # 发邮件
        # todo  这里是任务
        send_register_active_email.delay(email,username,token)

        # 返回应答,跳转到首页 这里是写的  url中的name
        return redirect(reversed('goods:index'))
# 激活
class ActiveView(View):
    '''用户激活'''
    def get(self,request,token):
        '''进行'''

        # 进行解密，获取激活的用户信息
        serializer = Serializer(settings.SECRET_KEY,3600)
        try:
            info = serializer.loads(token)
        #     获取待激活用户的id
            user_id = info['confirm']
        #     根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active=1
            user.save()
        #     跳转到登录页面
            return redirect(reversed('user:login'))
        except SignatureExpired as e:
        #    激活链接已过期
            return HttpResponse('激活链接已过期')
        pass

# 登录
class LoginView(View):
    '''登录'''
    def get(self,request):
        # 显示登录页面
        return render(request,'login.html')
