from django.urls import path
from .views import RegisterView, ActiveView, LoginView

app_name = 'user'

urlpatterns = [
    # path('register', views.register, name='register'),  # 注册页面

    path('register', RegisterView.as_view(), name='register'),  # 注册
    path('active/<token>', ActiveView.as_view(), name='active'),  # 用户激活
    path('login', LoginView.as_view(), name='login'),  # 用户登录
]
