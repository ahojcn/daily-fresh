from django.shortcuts import render, redirect
import re
from .models import User
from django.urls import reverse
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired
from django.conf import settings
from django.http import HttpResponse


# Create your views here.

# /user/register
# def register(request):
#     """显示注册页面"""
#     if request.method == 'GET':
#         # 显示注册页面
#         return render(request, 'register.html')
#     else:
#         # 进行注册处理
#         # 接收数据
#         username = request.POST.get('user_name')
#         password = request.POST.get('pwd')
#         email = request.POST.get('email')
#         allow = request.POST.get('allow')
#
#         # 数据校验
#         # 数据不完整
#         if not all([username, password, email]):
#             return render(request, 'register.html', {'errmsg': '数据不完整'})
#
#         # 校验邮箱
#         if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#             return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
#
#         # 是否同意用户协议
#         if allow != 'on':
#             return render(request, 'register.html', {'errmsg': '请同意协议'})
#
#         # 校验用户名是否重复
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             # 用户名不存在，可用
#             user = None
#
#         if user:
#             # 用户名已存在
#             return render(request, 'register.html', {'errmsg': '用户已存在'})
#
#         # 业务处理：用户注册
#         user = User.objects.create_user(username, email, password)
#         user.is_active = 0  # 不激活
#         user.save()
#
#         # 返回应答，跳转到首页
#         return redirect(reverse("goods:index"))

# /user/register
class RegisterView(View):
    """注册"""

    def get(self, request):
        """显示注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """进行注册处理"""

        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 数据校验
        # 数据不完整
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        # 是否同意用户协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在，可用
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户已存在'})

        # 业务处理：用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0  # 不激活
        user.save()

        # 发送激活邮件，包含激活链接
        # 激活链接中，需要包含用户的身份信息，并且身份信息要加密，使用 itsdangerous

        # 加密用户的身份信息，生成激活的 token（口令）
        s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = s.dumps(info)
        # print(' token0 '.center(50, '#'))
        # print(token)
        # print(' token1 '.center(50, '#'))
        pass
        # 发邮件

        # 返回应答，跳转到首页
        return redirect(reverse("goods:index"))


# /user/active/ + token
class ActiveView(View):
    """用户激活"""

    def get(self, request, token):
        """进行用户激活"""
        # 进行解密，获取要激活的用户信息
        s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        try:
            info = s.loads(token)
            # 获取待激活用户的 id
            userid = info['confirm']
            # 获取用户信息
            user = User.objects.get(id=userid)
            user.is_active = 1
            user.save()
            # 返回应答，跳转到登录页面
            # print(' 成功激活 '.center(50, '#'))
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接过期
            return HttpResponse('激活链接已过期')


# /user/login
class LoginView(View):
    """登录"""

    def get(self, request):
        """显示登录页面"""
        return render(request, 'login.html')
