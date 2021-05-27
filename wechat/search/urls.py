from . import views
from django.urls import path
from search import views

app_name = 'search'

urlpatterns = [
    path('', views.index),  # 首页
    path('login/', views.logins),  # 登录
    path('regist/', views.regist),  # 注册
    path('logout/', views.log_out),  # 登出
    path('search/', views.show_article, name='main'), # 搜索公众号

    path('search/<int:page>/', views.show_article, name='search'),
]
