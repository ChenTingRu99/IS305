from . import views
from django.urls import path
urlpatterns = [
    path('', views.index),  # 首页
    path('login/', views.logins),  # 登录
    path('regist/', views.regist),  # 注册
    path('logout/', views.log_out),  # 登出
]
