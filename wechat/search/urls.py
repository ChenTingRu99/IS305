from . import views
from django.urls import path
urlpatterns = [
    path('', views.index),  # 首页
]
