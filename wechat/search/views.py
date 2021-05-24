from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Articles
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from ...spider.getAccount import keyword_search_api
from ...spider.getArticles import get_articles_api

# Create your views here.


def index(request):
    linklist = Articles.objects.all()
    return render(request, 'search/index.html', {'linklist': linklist})


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


# search account by keyword
# data: keyword
# render directly or return json?
def search_account(request):

    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        result_list = keyword_search_api(keyword) # search account
        return render(request, 'search/searchResult.html', {'search_result': result_list})
    return render(request, 'search/search.html')


# show articles of the selected account
# data: account_name
# render?
def show_article(request):

    if request.method == 'GET':
        acc_name = request.GET.get('account_name')
        articles = get_articles_api(acc_name)
        return render(request, 'search/showArticles.html', {'articles': articles})

    return render(request, 'search/search.html')



