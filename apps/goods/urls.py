from django.urls import path, include
from . import views

app_name = 'goods'

urlpatterns = [
    path('', views.index, name='index'),  # 首页
]
