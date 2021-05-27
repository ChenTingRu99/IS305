from word.word_main import word_main
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import Articles, table_model_factory
from .tools import BaiduPaginator
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models.functions import Concat
from django.db.models import Value

import os
import sys
WORD_PATH = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.append(WORD_PATH)

SPIDER_PATH = os.path.abspath(os.path.join(
    __file__, os.pardir, os.pardir, os.pardir))
sys.path.append(SPIDER_PATH)
from spider.getArticles import get_articles_api

# Create your views here.


def index(request):
    linklist = Articles.objects.all()
    cy=''
    if request.method == "POST":
        word_url = request.POST.get("word_url")
        cy=word_url
        word_url = [word_url]
        word_main(word_url)
    return render(request, 'search/index.html', {'linklist': linklist[0:6],'cy':cy})


def logins(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            message = "用户名或密码错误!"
            return render(request, 'search/login.html', locals())
    return render(request, 'search/login.html')


def regist(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        if password1 != password2:
            message1 = '两次输入的密码不一样！'
            return render(request, 'search/regist.html', locals())
        else:
            if(User.objects.filter(username=username)):
                message3 = '用户已经存在，请重新选择用户名！'
                return render(request, 'search/regist.html', locals())

        cuser = User.objects.create_user(
            username=username, password=password1, email=email)
        cuser.save()
        return redirect('../login/')
    return render(request, 'search/regist.html')


def log_out(request):
    logout(request)
    return redirect('/')


def show_article(request, page=1):
    if request.method == 'GET':
        acc_name = request.GET.get('keyword')
        if not acc_name:
            return render(request, 'search/search.html')
        print(f'acc_name: {acc_name}')
        articles = get_articles_api(acc_name)
        JsonResponse({'articles': articles})
    tableNames = acc_name
    new_N = table_model_factory(tableNames)

    if request.user.is_active:
        userid = request.user.id
        current_user=User.objects.get(id=userid)
        history = current_user.first_name
        
        if history != '':
            User.objects.filter(id=userid).update(first_name=Concat(Value(history),Value(',')))    
            history = User.objects.get(id=userid).first_name
            User.objects.filter(id=userid).update(first_name=Concat(Value(history),Value(str(acc_name))))
        else:
            User.objects.filter(id=userid).update(first_name=Value(str(acc_name)))

    linklist = new_N.objects.all()
    
    # 产生分页器
    paginator = BaiduPaginator(linklist, 8)
    print(paginator.count)
    print(paginator.per_page)
    print(page)
    # 返回第page页的数据
    pager = paginator.page(page)
    pager.page_range = paginator.custom_range(paginator.num_pages, page, 5)

    return render(request, 'search/search.html', locals())
